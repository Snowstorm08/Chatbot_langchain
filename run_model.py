import os
import json
import time
import pickle
import torch

from transformers import AutoModelForCausalLM, AutoTokenizer
from llama_index.core import PromptTemplate, Settings
from llama_index.llms.huggingface import HuggingFaceLLM

from utils import log_time, LLM_MODEL_NAME, EMBEDDING_MODEL_NAME

# ==============================================================================
# DEVICE SELECTION (CUDA → MPS → CPU)
# ==============================================================================
def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


DEVICE = get_device()
log_time(f"Using device: {DEVICE}")

# ==============================================================================
# PATHS
# ==============================================================================
MODEL_ROOT = "./models"
INDEX_PATH = os.path.join(MODEL_ROOT, "index.pkl")
MODEL_PATH = os.path.join(MODEL_ROOT, "llm_model")
TOKENIZER_PATH = os.path.join(MODEL_ROOT, "llm_tokenizer")
EMBED_MODEL_PATH = os.path.join(MODEL_ROOT, "embedding_model_cpu.pkl")
LLM_CONFIG_PATH = os.path.join(MODEL_ROOT, "llm_config.json")

# ==============================================================================
# LOADERS
# ==============================================================================
def load_pickle(path, label):
    with open(path, "rb") as f:
        obj = pickle.load(f)
    log_time(f"{label} loaded ✔")
    return obj


def load_index():
    return load_pickle(INDEX_PATH, "Vector index")


def load_embedding_model():
    return load_pickle(EMBED_MODEL_PATH, "Embedding model")


def load_llm_config():
    with open(LLM_CONFIG_PATH, "r") as f:
        config = json.load(f)
    log_time("LLM config loaded ✔")
    return config


def load_model_and_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        torch_dtype=torch.float16 if DEVICE.type != "cpu" else torch.float32,
    )

    model.to(DEVICE)
    model.eval()

    log_time("Model & tokenizer loaded ✔")
    return model, tokenizer


# ==============================================================================
# LLM INITIALIZATION
# ==============================================================================
def initialize_llm(llm_config, model, tokenizer):
    llm = HuggingFaceLLM(
        context_window=llm_config["context_window"],
        max_new_tokens=llm_config["max_new_tokens"],
        generate_kwargs=llm_config["generate_kwargs"],
        system_prompt=llm_config["system_prompt"],
        query_wrapper_prompt=PromptTemplate(
            "<|USER|>{query_str}<|ASSISTANT|>"
        ),
        model=model,
        tokenizer=tokenizer,
    )

    log_time("HuggingFace LLM initialized ✔")
    return llm


def configure_settings(embed_model, llm):
    Settings.embed_model = embed_model
    Settings.llm = llm
    Settings.chunk_size = 1024
    log_time("LlamaIndex settings configured ✔")


# ==============================================================================
# TEXT GENERATION
# ==============================================================================
@torch.no_grad()
def generate_response(model, tokenizer, prompt, max_tokens=50):
    try:
        log_time("Tokenizing input...")
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(DEVICE)

        log_time("Generating response...")
        start = time.time()

        output = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            pad_token_id=tokenizer.eos_token_id
        )

        elapsed = time.time() - start
        log_time(f"Response generated in {elapsed:.2f}s")

        response = tokenizer.decode(
            output[0][inputs["input_ids"].shape[-1]:],
            skip_special_tokens=True
        )

        return response.strip()

    except Exception as e:
        log_time(f"Generation failed ❌ {e}")
        return None


# ==============================================================================
# INITIALIZATION PIPELINE
# ==============================================================================
def initialize_all():
    index = load_index()
    model, tokenizer = load_model_and_tokenizer()
    embed_model = load_embedding_model()
    llm_config = load_llm_config()

    llm = initialize_llm(llm_config, model, tokenizer)
    configure_settings(embed_model, llm)

    return {
        "index": index,
        "model": model,
        "tokenizer": tokenizer,
        "llm": llm,
    }


# ==============================================================================
# AUTO-INITIALIZE ON IMPORT
# ==============================================================================
STATE = initialize_all()
MODEL = STATE["model"]
TOKENIZER = STATE["tokenizer"]

# ==============================================================================
# EXAMPLE USAGE
# ==============================================================================
# question = "What is ECG (Electrocardiography)?"
# answer = generate_response(MODEL, TOKENIZER, question)
# print(answer)

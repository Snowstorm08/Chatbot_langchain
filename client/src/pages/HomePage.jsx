import { useCallback } from "react";
import { HeroHighlight, HackerText } from "../components";

const HomePage = () => {
  const focusStyles =
    "focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-950";

  const handleNavigation = useCallback(() => {
    window.location.href = "/chat";
  }, []);

  return (
    <HeroHighlight>
      <main
        className="
          min-h-screen
          flex
          items-center
          justify-center
          px-6
          py-12
          font-mono
        "
      >
        <section
          className="
            flex
            max-w-4xl
            flex-col
            items-center
            text-center
          "
        >
          {/* Title */}
          <HackerText
            text="Welcome to Revlis Chat"
            styles="
              mb-5
              text-4xl
              font-bold
              tracking-tight
              text-white
              sm:text-5xl
              lg:text-6xl
            "
          />

          {/* Subtitle */}
          <h2
            className="
              mb-5
              text-lg
              font-medium
              text-slate-300
              sm:text-xl
            "
          >
            Your Personalized Medical Assistant
          </h2>

          {/* Description */}
          <p
            className="
              mb-8
              max-w-3xl
              text-sm
              leading-7
              text-slate-400
              sm:text-base
            "
          >
            Welcome to our state-of-the-art AI medical assistant powered by
            advanced LLM technology. Revlis Chat uses a fine-tuned LLaMA model
            trained on extensive medical literature to provide accurate,
            contextual, and helpful responses to your health-related questions.
          </p>

          {/* CTA Button */}
          <button
            type="button"
            onClick={handleNavigation}
            className={`
              group
              relative
              inline-flex
              h-12
              overflow-hidden
              rounded-xl
              p-[1px]
              transition-all
              duration-300
              hover:scale-[1.02]
              active:scale-[0.98]
              ${focusStyles}
            `}
          >
            {/* Animated Border */}
            <span
              className="
                absolute
                inset-[-1000%]
                animate-[spin_3s_linear_infinite]
                bg-[conic-gradient(from_90deg_at_50%_50%,#E2CBFF_0%,#393BB2_50%,#E2CBFF_100%)]
              "
            />

            {/* Inner Content */}
            <span
              className="
                inline-flex
                h-full
                w-full
                items-center
                justify-center
                rounded-xl
                bg-slate-950
                px-8
                text-sm
                font-semibold
                text-white
                backdrop-blur-3xl
                transition-colors
                duration-200
                group-hover:bg-slate-900
              "
            >
              Start Chat
            </span>
          </button>
        </section>
      </main>
    </HeroHighlight>
  );
};

export default HomePage;

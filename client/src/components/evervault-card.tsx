"use client";

import React, { useCallback, useMemo } from "react";
import { motion, useMotionTemplate, useMotionValue } from "framer-motion";
import { cn } from "../utils/cn";

type EvervaultCardProps = {
  text?: string;
  className?: string;
};

export const EvervaultCard: React.FC<EvervaultCardProps> = ({
  text = "",
  className,
}) => {
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  // ✅ Generate once only
  const randomString = useMemo(() => generateRandomString(1500), []);

  // ✅ No state updates on mouse move
  const onMouseMove = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      const { left, top } = e.currentTarget.getBoundingClientRect();
      mouseX.set(e.clientX - left);
      mouseY.set(e.clientY - top);
    },
    [mouseX, mouseY]
  );

  return (
    <div
      className={cn(
        "p-0.5 bg-transparent aspect-square flex items-center justify-center w-full h-full relative",
        className
      )}
    >
      <div
        onMouseMove={onMouseMove}
        className="group/card rounded-3xl w-full h-full relative overflow-hidden flex items-center justify-center"
      >
        <CardPattern
          mouseX={mouseX}
          mouseY={mouseY}
          randomString={randomString}
        />

        <div className="relative z-10 flex items-center justify-center">
          <div className="relative h-44 w-44 rounded-full flex items-center justify-center text-4xl font-bold">
            <div className="absolute inset-0 bg-white/80 dark:bg-black/80 blur-sm rounded-full" />
            <span className="dark:text-white text-black z-20">
              {text}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

type CardPatternProps = {
  mouseX: any;
  mouseY: any;
  randomString: string;
};

export const CardPattern: React.FC<CardPatternProps> = ({
  mouseX,
  mouseY,
  randomString,
}) => {
  const maskImage = useMotionTemplate`
    radial-gradient(250px at ${mouseX}px ${mouseY}px, white, transparent)
  `;

  const style = {
    maskImage,
    WebkitMaskImage: maskImage,
  };

  return (
    <div className="pointer-events-none absolute inset-0">
      {/* Subtle top fade */}
      <div className="absolute inset-0 rounded-2xl [mask-image:linear-gradient(white,transparent)]" />

      {/* Gradient glow layer */}
      <motion.div
        style={style}
        className="absolute inset-0 rounded-2xl bg-gradient-to-r from-green-500 to-blue-700 opacity-0 group-hover/card:opacity-100 transition-opacity duration-500 will-change-transform"
      />

      {/* Matrix text layer */}
      <motion.div
        style={style}
        className="absolute inset-0 rounded-2xl opacity-0 mix-blend-overlay group-hover/card:opacity-100 transition-opacity duration-500"
      >
        <p className="absolute inset-0 text-xs break-words whitespace-pre-wrap text-white font-mono font-bold select-none">
          {randomString}
        </p>
      </motion.div>
    </div>
  );
};

/* ---------------- Utilities ---------------- */

const characters =
  "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

export const generateRandomString = (length: number): string => {
  let result = "";
  const charactersLength = characters.length;

  for (let i = 0; i < length; i++) {
    result += characters.charAt(
      Math.floor(Math.random() * charactersLength)
    );
  }

  return result;
};

/* ---------------- Icon ---------------- */

type IconProps = React.SVGProps<SVGSVGElement>;

export const Icon: React.FC<IconProps> = ({ className, ...rest }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
      className={className}
      {...rest}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M12 6v12m6-6H6"
      />
    </svg>
  );
};

import React from "react";
import { Compass, Heart } from "lucide-react";

export default function Footer() {
  return (
    <footer className="w-full border-t border-parchment-dark bg-parchment-base py-8 text-brown-light/80">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
          {/* Logo Brand */}
          <div className="flex items-center gap-2">
            <Compass className="h-4 w-4 text-gold-dark" />
            <span className="font-serif text-sm font-semibold tracking-wide text-brown-dark">
              ChronoPath AI
            </span>
          </div>

          {/* Description */}
          <p className="text-center text-xs md:text-left">
            Uncovering history in real time. Powered by Advanced AI Agent Architectures.
          </p>

          {/* Copyright / Attribution */}
          <div className="flex items-center gap-1 text-xs">
            <span>&copy; {new Date().getFullYear()} ChronoPath AI.</span>
            <span className="text-brown-light/40">|</span>
            <span className="flex items-center gap-0.5">
              Made with <Heart className="h-3 w-3 fill-gold-dark text-gold-dark" /> for exploration
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}

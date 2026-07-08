"use client";

import React from "react";
import { motion } from "framer-motion";
import { Compass, Sparkles, MapPin, AudioLines, Eye } from "lucide-react";

interface LandingScreenProps {
  onStart: () => void;
}

export default function LandingScreen({ onStart }: LandingScreenProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 sm:px-6">
      {/* Hero Content */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center max-w-3xl"
      >
        <div className="inline-flex items-center gap-2 rounded-full border border-gold-base/30 bg-gold-base/5 px-4 py-1.5 text-sm font-medium text-gold-dark mb-6">
          <Sparkles className="h-4 w-4 animate-pulse" />
          <span>Multimodal AI-Powered Storytelling</span>
        </div>

        <h1 className="font-serif text-4xl sm:text-6xl font-bold tracking-tight text-brown-dark leading-tight mb-6">
          Travel Through Time with <span className="text-gold-dark font-normal italic">ChronoPath AI</span>
        </h1>

        <p className="text-lg sm:text-xl text-brown-light/80 font-sans max-w-2xl mx-auto leading-relaxed mb-10">
          Unveil the hidden history beneath your feet. Discover historical stories, listen to audio chronicles, and view historical visualizations generated dynamically based on your physical location.
        </p>

        {/* Call to action */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.98 }}
          onClick={onStart}
          className="relative inline-flex items-center gap-3 bg-brown-base text-gold-base px-8 py-4 rounded-xl text-lg font-medium shadow-xl hover:bg-brown-light hover:text-gold-bright transition-all duration-300 group cursor-pointer focus:outline-none"
        >
          <Compass className="h-6 w-6 group-hover:rotate-45 transition-transform duration-300" />
          <span>Start Your Journey</span>
        </motion.button>
      </motion.div>

      {/* Feature Grid */}
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mt-24 w-full"
      >
        {/* Feature 1 */}
        <div className="parchment-card p-6 rounded-2xl flex flex-col gap-4">
          <div className="h-12 w-12 rounded-xl bg-brown-base/5 flex items-center justify-center text-brown-base border border-brown-base/10">
            <MapPin className="h-6 w-6 text-gold-dark" />
          </div>
          <div>
            <h3 className="font-serif text-lg font-bold text-brown-dark mb-2">Location Awareness</h3>
            <p className="text-sm text-brown-light/80 leading-relaxed">
              Detects nearby historical markers, landmarks, and battles using high-precision GPS positioning.
            </p>
          </div>
        </div>

        {/* Feature 2 */}
        <div className="parchment-card p-6 rounded-2xl flex flex-col gap-4">
          <div className="h-12 w-12 rounded-xl bg-brown-base/5 flex items-center justify-center text-brown-base border border-brown-base/10">
            <AudioLines className="h-6 w-6 text-gold-dark" />
          </div>
          <div>
            <h3 className="font-serif text-lg font-bold text-brown-dark mb-2">Audio Chronicles</h3>
            <p className="text-sm text-brown-light/80 leading-relaxed">
              Listen to professionally voiced narrative voiceovers detailing historical moments, cultures, and legends.
            </p>
          </div>
        </div>

        {/* Feature 3 */}
        <div className="parchment-card p-6 rounded-2xl flex flex-col gap-4">
          <div className="h-12 w-12 rounded-xl bg-brown-base/5 flex items-center justify-center text-brown-base border border-brown-base/10">
            <Eye className="h-6 w-6 text-gold-dark" />
          </div>
          <div>
            <h3 className="font-serif text-lg font-bold text-brown-dark mb-2">AI Visualizations</h3>
            <p className="text-sm text-brown-light/80 leading-relaxed">
              Witness the past. Dynamically generated historical images show what the location looked like centuries ago.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
}

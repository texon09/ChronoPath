"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Compass, CheckCircle2, Circle, Clock } from "lucide-react";

const STEPS = [
  { id: 0, label: "Acquiring coordinates & geolocation..." },
  { id: 1, label: "Scanning historical archives & Wikipedia..." },
  { id: 2, label: "Composing narrative story..." },
  { id: 3, label: "Synthesizing oral audio chronicle..." },
  { id: 4, label: "Reconstructing ancient visuals..." },
  { id: 5, label: "Preparing immersive portal..." },
];

export default function LoadingScreen() {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    // Progress through the steps every 1.5 seconds for visual storytelling impact
    const interval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev < STEPS.length - 1) {
          return prev + 1;
        }
        return prev;
      });
    }, 1800);

    return () => clearInterval(interval);
  }, []);

  const progressPercentage = ((currentStep + 1) / STEPS.length) * 100;

  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 sm:px-6">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="parchment-card w-full max-w-lg rounded-3xl p-8 flex flex-col items-center gap-8"
      >
        {/* Animated Compass Logo */}
        <div className="relative flex h-24 w-24 items-center justify-center rounded-full bg-brown-base/5 border border-gold-base/30 shadow-inner">
          <Compass className="h-12 w-12 text-gold-dark animate-spin-slow" />
          <div className="absolute inset-0 rounded-full border border-dashed border-gold-base/50 animate-spin-reverse" />
        </div>

        {/* Header Text */}
        <div className="text-center">
          <h2 className="font-serif text-2xl font-bold text-brown-dark">
            Opening Historical Pathway
          </h2>
          <p className="text-xs text-brown-light/70 flex items-center justify-center gap-1 mt-1 font-mono">
            <Clock className="h-3 w-3" />
            <span>Time Travel in Progress...</span>
          </p>
        </div>

        {/* Golden Progress Bar */}
        <div className="w-full h-2 bg-parchment-dark rounded-full overflow-hidden relative">
          <motion.div
            initial={{ width: "0%" }}
            animate={{ width: `${progressPercentage}%` }}
            transition={{ duration: 0.8 }}
            className="h-full bg-gradient-to-r from-gold-dark to-gold-bright rounded-full"
          />
        </div>

        {/* Step-by-Step Status List */}
        <div className="w-full flex flex-col gap-3">
          {STEPS.map((step) => {
            const isCompleted = currentStep > step.id;
            const isActive = currentStep === step.id;

            return (
              <div
                key={step.id}
                className={`flex items-center gap-3 p-3 rounded-xl border transition-all duration-300 ${
                  isActive
                    ? "bg-gold-base/5 border-gold-base/40 text-brown-dark shadow-sm scale-[1.02]"
                    : "border-transparent text-brown-light/50"
                } ${isCompleted ? "text-brown-light/80" : ""}`}
              >
                {isCompleted ? (
                  <CheckCircle2 className="h-5 w-5 text-gold-dark shrink-0" />
                ) : isActive ? (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                    className="shrink-0"
                  >
                    <Compass className="h-5 w-5 text-gold-dark" />
                  </motion.div>
                ) : (
                  <Circle className="h-5 w-5 text-brown-light/20 shrink-0" />
                )}
                
                <span className={`text-sm font-medium ${isActive ? "font-semibold" : ""}`}>
                  {step.label}
                </span>
              </div>
            );
          })}
        </div>

        <p className="text-[11px] text-brown-light/40 font-mono text-center">
          Building temporal maps using satellite coordinates
        </p>
      </motion.div>
    </div>
  );
}

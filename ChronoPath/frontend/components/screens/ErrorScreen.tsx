"use client";

import React from "react";
import { AlertTriangle, WifiOff, MapPinOff, ServerCrash, RefreshCw, ArrowLeft } from "lucide-react";
import { motion } from "framer-motion";

export type ErrorType = "NO_INTERNET" | "LOCATION_DENIED" | "SERVER_UNAVAILABLE" | "GENERATION_FAILED";

interface ErrorScreenProps {
  type: ErrorType;
  message?: string;
  onRetry: () => void;
  onBack: () => void;
}

export default function ErrorScreen({ type, message, onRetry, onBack }: ErrorScreenProps) {
  const getErrorDetails = () => {
    switch (type) {
      case "NO_INTERNET":
        return {
          icon: WifiOff,
          title: "Network Unreachable",
          desc: "It seems you are offline. ChronoPath AI requires an active internet connection to download local historical data and compile oral chronicles.",
        };
      case "LOCATION_DENIED":
        return {
          icon: MapPinOff,
          title: "Location Access Denied",
          desc: "We cannot scan histories without your coordinates. Please enable GPS location services in your browser/device settings to proceed.",
        };
      case "SERVER_UNAVAILABLE":
        return {
          icon: ServerCrash,
          title: "Temporal Link Offline",
          desc: "Our historical servers are currently unreachable. The server may be reloading or undergoing maintenance.",
        };
      case "GENERATION_FAILED":
      default:
        return {
          icon: AlertTriangle,
          title: "Chronicle Composition Failed",
          desc: "Something went wrong while compiling the story. This can happen if the location coordinates lack documented histories or the AI agents encountered a glitch.",
        };
    }
  };

  const { icon: Icon, title, desc } = getErrorDetails();

  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 sm:px-6">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
        className="parchment-card w-full max-w-md rounded-2xl p-8 text-center flex flex-col items-center gap-6"
      >
        {/* Error icon circle */}
        <div className="flex h-16 w-16 items-center justify-center rounded-full bg-red-50 border border-red-200 text-red-600 shadow-sm">
          <Icon className="h-8 w-8" />
        </div>

        <div className="text-center">
          <h2 className="font-serif text-xl font-bold text-brown-dark">{title}</h2>
          <p className="text-sm text-brown-light/80 leading-relaxed mt-2">{message || desc}</p>
        </div>

        <div className="flex flex-col gap-3 w-full border-t border-parchment-dark pt-6">
          <button
            onClick={onRetry}
            className="w-full flex items-center justify-center gap-2 bg-brown-base text-gold-base py-3 px-6 rounded-xl font-semibold shadow-md hover:bg-brown-light hover:text-gold-bright transition-all cursor-pointer focus:outline-none"
          >
            <RefreshCw className="h-4 w-4" />
            <span>Try Again</span>
          </button>

          <button
            onClick={onBack}
            className="w-full flex items-center justify-center gap-2 border border-parchment-dark bg-parchment-light hover:bg-parchment-dark/30 text-brown-light hover:text-brown-dark py-3 px-6 rounded-xl font-semibold transition-all cursor-pointer focus:outline-none"
          >
            <ArrowLeft className="h-4 w-4" />
            <span>Return to Map</span>
          </button>
        </div>
      </motion.div>
    </div>
  );
}

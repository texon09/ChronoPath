"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { Navigation, ShieldAlert, ArrowRight, Compass } from "lucide-react";

interface PermissionScreenProps {
  onPermissionGranted: (coords: { lat: number; lng: number }) => void;
  onPermissionDenied: (errorMsg: string) => void;
}

export default function PermissionScreen({
  onPermissionGranted,
  onPermissionDenied,
}: PermissionScreenProps) {
  const [requesting, setRequesting] = useState(false);

  const handleRequestLocation = () => {
    setRequesting(true);

    if (!navigator.geolocation) {
      const errorMsg = "Geolocation is not supported by your browser.";
      onPermissionDenied(errorMsg);
      setRequesting(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        onPermissionGranted({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        });
        setRequesting(false);
      },
      (error) => {
        let errorMsg = "Location access was denied.";
        if (error.code === error.PERMISSION_DENIED) {
          errorMsg = "Location access denied. Please enable location settings in your browser.";
        } else if (error.code === error.POSITION_UNAVAILABLE) {
          errorMsg = "Location information is unavailable.";
        } else if (error.code === error.TIMEOUT) {
          errorMsg = "The request to get your location timed out.";
        }
        onPermissionDenied(errorMsg);
        setRequesting(false);
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
  };

  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 sm:px-6">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="parchment-card w-full max-w-md rounded-2xl p-8 text-center flex flex-col items-center gap-6"
      >
        {/* Animated Icon */}
        <div className="relative flex h-20 w-20 items-center justify-center rounded-full bg-gold-base/10 border border-gold-base/30">
          <Navigation className="h-10 w-10 text-gold-dark animate-pulse" />
          <div className="absolute inset-0 rounded-full border border-gold-base/40 animate-ping opacity-25" />
        </div>

        <div>
          <h2 className="font-serif text-2xl font-bold text-brown-dark mb-3">
            Access Historical Pathways
          </h2>
          <p className="text-sm text-brown-light/80 leading-relaxed">
            ChronoPath AI requires access to your physical location to uncover historical landmarks, ancient stories, and local battles in your immediate surroundings.
          </p>
        </div>

        {/* Privacy Note */}
        <div className="flex items-start gap-2 text-left bg-gold-base/5 border border-gold-base/20 rounded-xl p-4 w-full">
          <ShieldAlert className="h-5 w-5 text-gold-dark shrink-0 mt-0.5" />
          <span className="text-xs text-brown-light leading-relaxed">
            Your coordinates are used strictly in real-time to load nearby histories and generate AI narration. We do not store or track your continuous movement.
          </span>
        </div>

        {/* Buttons */}
        <button
          onClick={handleRequestLocation}
          disabled={requesting}
          className="w-full flex items-center justify-center gap-2 bg-brown-base text-gold-base py-3.5 px-6 rounded-xl font-medium shadow-md hover:bg-brown-light hover:text-gold-bright disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 group cursor-pointer focus:outline-none"
        >
          {requesting ? (
            <>
              <Compass className="h-5 w-5 animate-spin" />
              <span>Requesting GPS Access...</span>
            </>
          ) : (
            <>
              <span>Allow Location Access</span>
              <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
            </>
          )}
        </button>
      </motion.div>
    </div>
  );
}

"use client";

import React, { useState } from "react";
import { Maximize2, Download, Minimize2, ZoomIn, Eye } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface ImageViewerProps {
  url: string;
  placeName: string;
}

export default function ImageViewer({ url, placeName }: ImageViewerProps) {
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [imageError, setImageError] = useState(false);

  const handleDownload = async () => {
    try {
      const response = await fetch(url);
      const blob = await response.blob();
      const blobUrl = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = blobUrl;
      link.download = `${placeName.replace(/\s+/g, "_")}_historical_reconstruction.jpg`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(blobUrl);
    } catch (e) {
      // Fallback: Open URL in new window if download blocks due to CORS
      window.open(url, "_blank");
    }
  };

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  if (imageError) {
    return null; // Don't show anything or show small placeholder if URL is broken
  }

  return (
    <>
      <div className="relative group overflow-hidden rounded-2xl border border-parchment-dark bg-parchment-base aspect-video w-full shadow-md flex items-center justify-center">
        {/* Main image */}
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={url}
          alt={`Historical reconstruction of ${placeName}`}
          onError={() => setImageError(true)}
          className="object-cover w-full h-full hover:scale-105 transition-transform duration-700"
        />

        {/* Backdrop vignette overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-brown-dark/70 via-transparent to-transparent opacity-60 group-hover:opacity-85 transition-opacity" />

        {/* Caption */}
        <div className="absolute bottom-4 left-4 flex flex-col text-left text-parchment-light z-10">
          <span className="text-[10px] uppercase font-bold tracking-wider text-gold-bright">
            AI Visual Reconstruction
          </span>
          <h4 className="font-serif text-sm font-semibold tracking-wide mt-0.5 drop-shadow-sm">
            {placeName} in historical era
          </h4>
        </div>

        {/* Floating actions */}
        <div className="absolute top-4 right-4 flex items-center gap-2 z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
          <button
            onClick={toggleFullscreen}
            className="flex h-9 w-9 items-center justify-center rounded-lg bg-brown-base/80 border border-gold-base/30 text-gold-base hover:bg-brown-light hover:text-gold-bright hover:scale-105 transition-all shadow-md focus:outline-none"
            title="Expand Image"
          >
            <Maximize2 className="h-4 w-4" />
          </button>
          <button
            onClick={handleDownload}
            className="flex h-9 w-9 items-center justify-center rounded-lg bg-brown-base/80 border border-gold-base/30 text-gold-base hover:bg-brown-light hover:text-gold-bright hover:scale-105 transition-all shadow-md focus:outline-none"
            title="Download Image"
          >
            <Download className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Expanded Lightbox Modal */}
      <AnimatePresence>
        {isFullscreen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-brown-dark/95 flex flex-col items-center justify-center p-4 backdrop-blur-md"
          >
            {/* Top Bar controls */}
            <div className="absolute top-4 left-4 right-4 flex items-center justify-between text-parchment-light z-10">
              <h3 className="font-serif text-lg font-bold tracking-wide">
                {placeName} Reconstructed
              </h3>
              <div className="flex gap-2">
                <button
                  onClick={handleDownload}
                  className="flex h-10 w-10 items-center justify-center rounded-lg bg-brown-base hover:bg-brown-light text-gold-base border border-gold-base/30 transition-all focus:outline-none"
                >
                  <Download className="h-5 w-5" />
                </button>
                <button
                  onClick={toggleFullscreen}
                  className="flex h-10 w-10 items-center justify-center rounded-lg bg-brown-base hover:bg-brown-light text-gold-base border border-gold-base/30 transition-all focus:outline-none"
                >
                  <Minimize2 className="h-5 w-5" />
                </button>
              </div>
            </div>

            {/* Lightbox Image Container */}
            <motion.div
              initial={{ scale: 0.95 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.95 }}
              className="relative max-w-5xl max-h-[80vh] w-full h-full flex items-center justify-center rounded-2xl overflow-hidden border border-gold-base/20 shadow-2xl"
            >
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={url}
                alt={placeName}
                className="max-w-full max-h-full object-contain"
              />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

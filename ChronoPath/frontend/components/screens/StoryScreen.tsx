"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { Copy, Share2, Compass, Check, BookOpen, Clock } from "lucide-react";
import { GenerateResponse } from "../../types";
import AudioPlayer from "../AudioPlayer";
import ImageViewer from "../ImageViewer";

interface StoryScreenProps {
  data: GenerateResponse;
  onExploreMore: () => void;
}

export default function StoryScreen({ data, onExploreMore }: StoryScreenProps) {
  const [copied, setCopied] = useState(false);
  const [shared, setShared] = useState(false);

  const placeName = typeof data.place === "string" ? data.place : data.place.name;
  const { title, story } = data.text;

  // Calculate estimated reading time
  const wordCount = story.split(/\s+/).length;
  const readingTime = Math.max(1, Math.ceil(wordCount / 180)); // 180 words per minute average

  const handleCopy = () => {
    navigator.clipboard.writeText(`${title}\n\n${story}`).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator
        .share({
          title: `Discover ${placeName} | ChronoPath AI`,
          text: `Read about: ${title}`,
          url: window.location.href,
        })
        .catch(() => {
          setShared(true);
          setTimeout(() => setShared(false), 2000);
        });
    } else {
      navigator.clipboard.writeText(window.location.href).then(() => {
        setShared(true);
        setTimeout(() => setShared(false), 2000);
      });
    }
  };

  return (
    <div className="mx-auto max-w-3xl px-4 py-8 flex flex-col gap-6">
      {/* Story Layout Header card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="parchment-card rounded-2xl p-6 sm:p-8 flex flex-col gap-4"
      >
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-parchment-dark pb-4">
          <div className="flex flex-col text-left">
            <span className="text-[10px] uppercase font-bold tracking-wider text-gold-dark">
              {placeName}
            </span>
            <h2 className="font-serif text-2xl sm:text-3xl font-extrabold text-brown-dark mt-1">
              {title}
            </h2>
          </div>

          {/* Reading Time */}
          <div className="flex items-center gap-1.5 text-xs text-brown-light/70 font-mono bg-parchment-dark/40 px-3 py-1.5 rounded-lg">
            <Clock className="h-4 w-4 text-gold-dark" />
            <span>{readingTime} Min Read</span>
          </div>
        </div>

        {/* Story Text */}
        <div className="font-serif text-base sm:text-lg text-brown-light leading-relaxed text-justify whitespace-pre-wrap py-2">
          {story}
        </div>

        {/* Bottom Actions Row */}
        <div className="flex items-center justify-between border-t border-parchment-dark pt-4 mt-2">
          <div className="flex gap-2">
            <button
              onClick={handleCopy}
              className="flex items-center gap-2 border border-parchment-dark hover:bg-parchment-dark/30 text-brown-light hover:text-brown-dark px-3 py-2 rounded-lg text-xs font-semibold transition-all focus:outline-none"
            >
              {copied ? (
                <>
                  <Check className="h-3.5 w-3.5 text-gold-dark" />
                  <span>Copied!</span>
                </>
              ) : (
                <>
                  <Copy className="h-3.5 w-3.5" />
                  <span>Copy Story</span>
                </>
              )}
            </button>

            <button
              onClick={handleShare}
              className="flex items-center gap-2 border border-parchment-dark hover:bg-parchment-dark/30 text-brown-light hover:text-brown-dark px-3 py-2 rounded-lg text-xs font-semibold transition-all focus:outline-none"
            >
              <Share2 className="h-3.5 w-3.5" />
              <span>{shared ? "Link Copied!" : "Share"}</span>
            </button>
          </div>

          <div className="flex items-center gap-1.5 text-xs font-semibold text-gold-dark">
            <BookOpen className="h-4 w-4" />
            <span>ChronoPath Chronicle</span>
          </div>
        </div>
      </motion.div>

      {/* Multimodal integrations (Audio & Image) */}
      {(data.audio?.url || data.visual?.url) && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.15 }}
          className="grid grid-cols-1 md:grid-cols-2 gap-6"
        >
          {/* Custom audio player */}
          {data.audio?.url && (
            <div className="md:col-span-2">
              <AudioPlayer url={data.audio.url} duration={data.audio.duration} />
            </div>
          )}

          {/* Historical reconstruction image */}
          {data.visual?.url && (
            <div className="md:col-span-2">
              <ImageViewer url={data.visual.url} placeName={placeName} />
            </div>
          )}
        </motion.div>
      )}

      {/* Explore More CTA */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="flex justify-center mt-4"
      >
        <button
          onClick={onExploreMore}
          className="flex items-center gap-2 bg-brown-base text-gold-base px-6 py-3.5 rounded-xl font-bold shadow-md hover:bg-brown-light hover:text-gold-bright transition-all group focus:outline-none"
        >
          <Compass className="h-5 w-5 group-hover:rotate-45 transition-transform" />
          <span>Explore More Locations</span>
        </button>
      </motion.div>
    </div>
  );
}

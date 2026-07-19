"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Compass, Settings2, Sparkles, MapPin, Globe2 } from "lucide-react";
import Map from "../Map";
import { Profile } from "../../types";
import { getProfile, updateProfile } from "../../services/api";

interface JourneyScreenProps {
  latitude: number;
  longitude: number;
  onExplore: (options: {
    language?: string;
    age?: number;
    origin?: string;
    background?: string;
    name?: string;
  }) => void;
}

export default function JourneyScreen({
  latitude,
  longitude,
  onExplore,
}: JourneyScreenProps) {
  const [showSettings, setShowSettings] = useState(false);
  const [profile, setProfile] = useState<Profile | null>(null);

  // Editable settings fields
  const [name, setName] = useState("");
  const [language, setLanguage] = useState("English");
  const [age, setAge] = useState<number>(25);
  const [origin, setOrigin] = useState("");
  const [background, setBackground] = useState("");

  useEffect(() => {
    getProfile().then((prof) => {
      setProfile(prof);
      setName(prof.name || "");
      setLanguage(prof.preferredLanguage || "English");
      setAge(prof.age || 25);
      setOrigin(prof.origin || "");
      setBackground(prof.background || "");
    });
  }, []);

  const handleSaveSettings = async () => {
    const updated = await updateProfile({
      preferredLanguage: language,
      age,
      origin,
      background,
    });
    setProfile(updated);
    setShowSettings(false);
  };

  const handleExploreClick = () => {
    onExplore({
      name: name || undefined,
      language,
      age,
      origin: origin || undefined,
      background: background || undefined,
    });
  };

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 flex flex-col gap-6">
      {/* Location Bar & Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-parchment-base border border-parchment-dark p-4 rounded-xl">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-brown-base/5 border border-brown-base/10 text-gold-dark">
            <MapPin className="h-5 w-5" />
          </div>
          <div>
            <span className="text-[10px] uppercase font-bold text-brown-light/60 tracking-wider">
              Current GPS Coordinates
            </span>
            <div className="text-sm font-mono text-brown-dark font-medium mt-0.5">
              {latitude.toFixed(5)}° N, {longitude.toFixed(5)}° E
            </div>
          </div>
        </div>

        <button
          onClick={() => setShowSettings(!showSettings)}
          className="flex items-center justify-center gap-2 border border-parchment-dark bg-parchment-light hover:bg-parchment-dark/30 text-brown-light hover:text-brown-dark px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-300 focus:outline-none"
        >
          <Settings2 className="h-4 w-4" />
          <span>Story Preferences</span>
        </button>
      </div>

      {/* Main Map Box */}
      <div className="relative h-[350px] sm:h-[450px] w-full rounded-2xl overflow-hidden shadow-md border border-parchment-dark bg-parchment-base">
        <Map latitude={latitude} longitude={longitude} />

        {/* Floating Settings Panel */}
        <AnimatePresence>
          {showSettings && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              className="absolute inset-0 z-20 bg-parchment-light/95 backdrop-blur-sm p-6 overflow-y-auto flex flex-col justify-between"
            >
              <div className="flex flex-col gap-4">
                <div className="flex items-center justify-between border-b border-parchment-dark pb-3">
                  <h3 className="font-serif text-lg font-bold text-brown-dark flex items-center gap-2">
                    <Globe2 className="h-5 w-5 text-gold-dark" />
                    <span>Story Customization</span>
                  </h3>
                  <button
                    onClick={() => setShowSettings(false)}
                    className="text-xs text-brown-light hover:text-brown-dark underline"
                  >
                    Close
                  </button>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {/* Language Selector */}
                  <div className="flex flex-col gap-1.5">
                    <label className="text-xs font-semibold text-brown-light">Language</label>
                    <select
                      value={language}
                      onChange={(e) => setLanguage(e.target.value)}
                      className="border border-parchment-dark bg-parchment-base text-sm text-brown-dark rounded-lg p-2 focus:outline-none focus:ring-1 focus:ring-gold-base"
                    >
                      <option value="English">English</option>
                      <option value="Hindi">Hindi</option>
                      <option value="Marathi">Marathi</option>
                      <option value="Spanish">Spanish</option>
                      <option value="French">French</option>
                    </select>
                  </div>

                  {/* Age Input */}
                  <div className="flex flex-col gap-1.5">
                    <label className="text-xs font-semibold text-brown-light">Target Age Group</label>
                    <input
                      type="number"
                      value={age}
                      min={5}
                      max={120}
                      onChange={(e) => setAge(parseInt(e.target.value) || 25)}
                      className="border border-parchment-dark bg-parchment-base text-sm text-brown-dark rounded-lg p-2 focus:outline-none focus:ring-1 focus:ring-gold-base"
                    />
                  </div>

                  {/* Origin */}
                  <div className="flex flex-col gap-1.5">
                    <label className="text-xs font-semibold text-brown-light">User Origin / Nationality</label>
                    <input
                      type="text"
                      placeholder="e.g. Pune, India"
                      value={origin}
                      onChange={(e) => setOrigin(e.target.value)}
                      className="border border-parchment-dark bg-parchment-base text-sm text-brown-dark rounded-lg p-2 placeholder:text-brown-light/40 focus:outline-none focus:ring-1 focus:ring-gold-base"
                    />
                  </div>

                  {/* Background */}
                  <div className="flex flex-col gap-1.5 sm:col-span-2">
                    <label className="text-xs font-semibold text-brown-light">Your Background / Interests</label>
                    <textarea
                      placeholder="e.g. Interested in architecture and military histories."
                      value={background}
                      onChange={(e) => setBackground(e.target.value)}
                      rows={2}
                      className="border border-parchment-dark bg-parchment-base text-sm text-brown-dark rounded-lg p-2 placeholder:text-brown-light/40 focus:outline-none focus:ring-1 focus:ring-gold-base resize-none"
                    />
                  </div>
                </div>
              </div>

              <div className="flex gap-3 mt-6 border-t border-parchment-dark pt-4">
                <button
                  onClick={handleSaveSettings}
                  className="flex-1 bg-brown-base text-gold-base py-2.5 rounded-lg text-sm font-semibold hover:bg-brown-light transition-all"
                >
                  Save & Apply
                </button>
                <button
                  onClick={() => setShowSettings(false)}
                  className="flex-1 border border-parchment-dark text-brown-light py-2.5 rounded-lg text-sm font-semibold hover:bg-parchment-dark/30 transition-all"
                >
                  Cancel
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Explore Button Section */}
      <div className="flex flex-col items-center gap-4 mt-2">
        <button
          onClick={handleExploreClick}
          className="relative inline-flex items-center gap-3 bg-brown-base text-gold-base px-10 py-5 rounded-2xl text-xl font-bold shadow-xl hover:bg-brown-light hover:text-gold-bright hover:shadow-2xl transition-all duration-300 group cursor-pointer border border-gold-base/20 focus:outline-none"
        >
          <Compass className="h-6 w-6 group-hover:rotate-90 transition-transform duration-500 text-gold-dark" />
          <span>Explore Surroundings</span>
          <div className="absolute -top-1.5 -right-1.5 flex h-4 w-4">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-gold-bright opacity-75"></span>
            <span className="relative inline-flex rounded-full h-4 w-4 bg-gold-dark"></span>
          </div>
        </button>

        <p className="text-xs text-brown-light/70 text-center max-w-sm leading-relaxed">
          ChronoPath AI will query Wikipedia, historical datasets, and compile local chronicles to compose an immersive story.
        </p>
      </div>
    </div>
  );
}

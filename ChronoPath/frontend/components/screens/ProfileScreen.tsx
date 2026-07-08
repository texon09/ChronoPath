"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { User, BookOpen, MapPin, Globe, Save, Award, Check } from "lucide-react";
import { Profile } from "../../types";
import { getProfile, updateProfile } from "../../services/api";

export default function ProfileScreen() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);
  const [savedStatus, setSavedStatus] = useState(false);

  // Form states
  const [language, setLanguage] = useState("English");
  const [age, setAge] = useState<number>(25);
  const [origin, setOrigin] = useState("");
  const [background, setBackground] = useState("");

  useEffect(() => {
    getProfile().then((prof) => {
      setProfile(prof);
      setLanguage(prof.preferredLanguage || "English");
      setAge(prof.age || 25);
      setOrigin(prof.origin || "");
      setBackground(prof.background || "");
      setLoading(false);
    });
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    const updated = await updateProfile({
      preferredLanguage: language,
      age,
      origin,
      background,
    });
    setProfile(updated);
    setSavedStatus(true);
    setTimeout(() => setSavedStatus(false), 2000);
  };

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-gold-base border-t-transparent" />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-8 flex flex-col gap-6">
      {/* Header */}
      <div className="flex items-center gap-3 border-b border-parchment-dark pb-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brown-base text-gold-base shadow-sm">
          <User className="h-6 w-6" />
        </div>
        <div className="text-left">
          <h2 className="font-serif text-2xl font-bold text-brown-dark">Explorer Profile</h2>
          <p className="text-xs text-brown-light/70 font-semibold uppercase tracking-wider mt-0.5">
            Your Preferences & Statistics
          </p>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-4">
        <div className="parchment-card p-4 rounded-xl flex items-center gap-4 text-left">
          <div className="h-10 w-10 rounded-lg bg-brown-base/5 border border-brown-base/10 flex items-center justify-center text-gold-dark shrink-0">
            <BookOpen className="h-5 w-5" />
          </div>
          <div>
            <span className="text-[10px] uppercase font-bold text-brown-light/50 tracking-wider">
              Stories Read
            </span>
            <div className="text-xl font-bold text-brown-dark mt-0.5">
              {profile?.storiesViewedCount || 0}
            </div>
          </div>
        </div>

        <div className="parchment-card p-4 rounded-xl flex items-center gap-4 text-left">
          <div className="h-10 w-10 rounded-lg bg-brown-base/5 border border-brown-base/10 flex items-center justify-center text-gold-dark shrink-0">
            <Award className="h-5 w-5" />
          </div>
          <div>
            <span className="text-[10px] uppercase font-bold text-brown-light/50 tracking-wider">
              Places Visited
            </span>
            <div className="text-xl font-bold text-brown-dark mt-0.5">
              {profile?.placesVisitedCount || 0}
            </div>
          </div>
        </div>
      </div>

      {/* Preferences Form */}
      <form onSubmit={handleSave} className="parchment-card rounded-2xl p-6 sm:p-8 flex flex-col gap-5 text-left">
        <h3 className="font-serif text-lg font-bold text-brown-dark border-b border-parchment-dark pb-3">
          Chronicle Tuning parameters
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {/* Preferred Language */}
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-brown-light flex items-center gap-1">
              <Globe className="h-3.5 w-3.5" />
              <span>Preferred Language</span>
            </label>
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

          {/* Age Group */}
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-brown-light">Explorer Age</label>
            <input
              type="number"
              value={age}
              min={5}
              max={110}
              onChange={(e) => setAge(parseInt(e.target.value) || 25)}
              className="border border-parchment-dark bg-parchment-base text-sm text-brown-dark rounded-lg p-2 focus:outline-none focus:ring-1 focus:ring-gold-base"
            />
          </div>

          {/* Nationality / Origin */}
          <div className="flex flex-col gap-1.5 sm:col-span-2">
            <label className="text-xs font-semibold text-brown-light flex items-center gap-1">
              <MapPin className="h-3.5 w-3.5" />
              <span>Your Origin / Location Background</span>
            </label>
            <input
              type="text"
              placeholder="e.g. Maharashtra, India"
              value={origin}
              onChange={(e) => setOrigin(e.target.value)}
              className="border border-parchment-dark bg-parchment-base text-sm text-brown-dark rounded-lg p-2 placeholder:text-brown-light/40 focus:outline-none focus:ring-1 focus:ring-gold-base"
            />
          </div>

          {/* History Background Interest */}
          <div className="flex flex-col gap-1.5 sm:col-span-2">
            <label className="text-xs font-semibold text-brown-light">Historical Interests & Background</label>
            <textarea
              placeholder="e.g. Student of 18th century naval warfare and Maratha architecture."
              value={background}
              onChange={(e) => setBackground(e.target.value)}
              rows={3}
              className="border border-parchment-dark bg-parchment-base text-sm text-brown-dark rounded-lg p-2 placeholder:text-brown-light/40 focus:outline-none focus:ring-1 focus:ring-gold-base resize-none"
            />
            <span className="text-[10px] text-brown-light/50">
              The AI supervisor uses this to tailor vocabulary, references, and narrative details.
            </span>
          </div>
        </div>

        {/* Save Button */}
        <button
          type="submit"
          className="bg-brown-base text-gold-base py-3 px-6 rounded-xl font-semibold shadow-md hover:bg-brown-light hover:text-gold-bright flex items-center justify-center gap-2 cursor-pointer transition-all self-end mt-4 focus:outline-none"
        >
          {savedStatus ? (
            <>
              <Check className="h-4 w-4 text-gold-bright" />
              <span>Saved Successfully</span>
            </>
          ) : (
            <>
              <Save className="h-4 w-4" />
              <span>Save Changes</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}

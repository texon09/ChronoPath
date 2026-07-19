"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { History, MapPin, Calendar, Clock, BookOpen, Trash2 } from "lucide-react";
import { Journey } from "../../types";
import { getJourney } from "../../services/api";

export default function TimelineScreen() {
  const [journeys, setJourneys] = useState<Journey[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getJourney().then((history) => {
      setJourneys(history);
      setLoading(false);
    });
  }, []);

  const handleClearHistory = () => {
    if (confirm("Are you sure you want to clear your local journey timeline?")) {
      localStorage.removeItem("chronopath_journey_history");
      setJourneys([]);
    }
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
      {/* Page Header */}
      <div className="flex items-center justify-between border-b border-parchment-dark pb-4">
        <div className="flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brown-base text-gold-base shadow-sm">
            <History className="h-6 w-6" />
          </div>
          <div className="text-left">
            <h2 className="font-serif text-2xl font-bold text-brown-dark">Journey Timeline</h2>
            <p className="text-xs text-brown-light/70 font-semibold uppercase tracking-wider mt-0.5">
              Your Historical Log
            </p>
          </div>
        </div>

        {journeys.length > 0 && (
          <button
            onClick={handleClearHistory}
            className="flex items-center gap-1.5 border border-red-200 bg-red-50 hover:bg-red-100 text-red-700 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all focus:outline-none"
          >
            <Trash2 className="h-3.5 w-3.5" />
            <span>Clear Logs</span>
          </button>
        )}
      </div>

      {/* Timeline items list */}
      {journeys.length === 0 ? (
        <div className="parchment-card rounded-2xl p-8 text-center flex flex-col items-center gap-4">
          <div className="h-12 w-12 rounded-full bg-parchment-dark flex items-center justify-center text-brown-light/60">
            <MapPin className="h-6 w-6" />
          </div>
          <div>
            <h3 className="font-serif text-lg font-semibold text-brown-dark">No Visited Locations Yet</h3>
            <p className="text-sm text-brown-light/80 mt-1 max-w-sm">
              Your coordinates are saved here locally after exploring stories. Grant location permissions and click Explore to begin your path!
            </p>
          </div>
        </div>
      ) : (
        <div className="relative border-l border-gold-base/30 ml-4 pl-6 flex flex-col gap-8 py-2">
          {journeys.map((journey) => (
            <div key={journey.id} className="relative flex flex-col gap-4">
              {/* Timeline marker */}
              <div className="absolute -left-[31px] top-1 bg-parchment-light border border-gold-base p-1 rounded-full text-gold-dark z-10 shadow-sm">
                <Calendar className="h-4 w-4" />
              </div>

              {/* Date Header */}
              <h3 className="font-serif text-base font-bold text-brown-dark/90 tracking-wide text-left mt-0.5">
                {journey.date}
              </h3>

              {/* Grouped Places */}
              <div className="flex flex-col gap-3">
                {journey.places.map((place) => (
                  <motion.div
                    key={place.id}
                    whileHover={{ x: 2 }}
                    className="parchment-card p-4 rounded-xl flex items-start gap-4 transition-transform text-left"
                  >
                    <div className="h-10 w-10 rounded-lg bg-brown-base/5 border border-brown-base/10 flex items-center justify-center text-gold-dark shrink-0">
                      <MapPin className="h-5 w-5" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-2">
                        <h4 className="font-serif text-base font-bold text-brown-dark truncate">
                          {place.name}
                        </h4>
                        <span className="flex items-center gap-1 text-[10px] text-brown-light/60 font-mono">
                          <Clock className="h-3 w-3" />
                          <span>{place.timestamp}</span>
                        </span>
                      </div>
                      <p className="text-xs text-brown-light/80 mt-0.5 italic truncate">
                        {place.storyTitle}
                      </p>
                      <div className="text-[10px] font-mono text-brown-light/50 mt-2">
                        Lat: {place.latitude.toFixed(4)} | Lng: {place.longitude.toFixed(4)}
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

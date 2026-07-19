"use client";

import React, { useState, useRef, useEffect } from "react";
import { Play, Pause, Volume2, VolumeX, RotateCcw, AlertCircle } from "lucide-react";

interface AudioPlayerProps {
  url: string;
  duration?: string;
}

export default function AudioPlayer({ url, duration }: AudioPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [totalDuration, setTotalDuration] = useState(0);
  const [volume, setVolume] = useState(0.8);
  const [isMuted, setIsMuted] = useState(false);
  const [error, setError] = useState(false);

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const progressBarRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    setError(false);
    setIsPlaying(false);
    setCurrentTime(0);
    
    // Create new audio element to clean up legacy streams
    const audio = new Audio(url);
    audioRef.current = audio;
    audio.volume = volume;

    const onTimeUpdate = () => {
      setCurrentTime(audio.currentTime);
    };

    const onLoadedMetadata = () => {
      setTotalDuration(audio.duration || 0);
    };

    const onEnded = () => {
      setIsPlaying(false);
      setCurrentTime(0);
    };

    const onError = () => {
      setError(true);
      setIsPlaying(false);
    };

    audio.addEventListener("timeupdate", onTimeUpdate);
    audio.addEventListener("loadedmetadata", onLoadedMetadata);
    audio.addEventListener("ended", onEnded);
    audio.addEventListener("error", onError);

    return () => {
      audio.pause();
      audio.removeEventListener("timeupdate", onTimeUpdate);
      audio.removeEventListener("loadedmetadata", onLoadedMetadata);
      audio.removeEventListener("ended", onEnded);
      audio.removeEventListener("error", onError);
      audioRef.current = null;
    };
  }, [url]);

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = isMuted ? 0 : volume;
    }
  }, [volume, isMuted]);

  const togglePlay = () => {
    if (!audioRef.current || error) return;

    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      audioRef.current.play().then(() => {
        setIsPlaying(true);
      }).catch(() => {
        setError(true);
      });
    }
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const time = parseFloat(e.target.value);
    setCurrentTime(time);
    if (audioRef.current) {
      audioRef.current.currentTime = time;
    }
  };

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const vol = parseFloat(e.target.value);
    setVolume(vol);
    setIsMuted(vol === 0);
  };

  const toggleMute = () => {
    setIsMuted(!isMuted);
  };

  const formatTime = (time: number) => {
    if (isNaN(time)) return "00:00";
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
  };

  return (
    <div className="w-full bg-brown-base text-parchment-light rounded-2xl p-4 sm:p-6 shadow-lg border border-gold-base/20 flex flex-col gap-4">
      <div className="flex items-center justify-between gap-4">
        {/* Title */}
        <div className="flex flex-col">
          <span className="text-[10px] uppercase font-bold tracking-wider text-gold-base/60">
            Audio Narration
          </span>
          <span className="text-sm font-serif font-semibold text-gold-bright truncate max-w-[200px] sm:max-w-xs">
            Oral History Chronicle
          </span>
        </div>

        {/* Visualizer bars */}
        <div className="flex items-center gap-1 h-6">
          {[1, 2, 3, 4, 5, 6, 7, 8].map((bar) => (
            <div
              key={bar}
              style={{
                animationDelay: `${bar * 0.1}s`,
                height: isPlaying ? "100%" : "20%",
              }}
              className={`w-1 bg-gold-base rounded-full transition-all duration-300 ${
                isPlaying ? "animate-pulse" : ""
              }`}
            />
          ))}
        </div>
      </div>

      {error ? (
        <div className="flex items-center gap-2 text-red-400 bg-red-950/20 border border-red-900/30 p-3 rounded-lg text-xs">
          <AlertCircle className="h-4 w-4 shrink-0" />
          <span>Oral narrative audio stream unavailable. Please read the story instead.</span>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {/* Progress Slider */}
          <div className="flex items-center gap-3">
            <span className="text-xs font-mono text-gold-base/80">{formatTime(currentTime)}</span>
            <input
              ref={progressBarRef}
              type="range"
              min={0}
              max={totalDuration || 100}
              value={currentTime}
              onChange={handleSeek}
              className="flex-1 h-1.5 bg-brown-light rounded-lg appearance-none cursor-pointer accent-gold-base focus:outline-none"
            />
            <span className="text-xs font-mono text-gold-base/80">
              {formatTime(totalDuration || parseInt(duration || "0") || 0)}
            </span>
          </div>

          {/* Controls Bar */}
          <div className="flex items-center justify-between gap-4 pt-1">
            {/* Left: Quick Rewind */}
            <button
              onClick={() => {
                if (audioRef.current) audioRef.current.currentTime = 0;
              }}
              className="text-gold-base/70 hover:text-gold-bright focus:outline-none p-1 transition-colors"
              title="Restart Audio"
            >
              <RotateCcw className="h-4 w-4" />
            </button>

            {/* Middle: Main Play Button */}
            <button
              onClick={togglePlay}
              className="flex h-12 w-12 items-center justify-center rounded-full bg-gold-base text-brown-dark shadow hover:bg-gold-bright transition-all focus:outline-none cursor-pointer"
            >
              {isPlaying ? <Pause className="h-6 w-6" /> : <Play className="h-6 w-6 fill-brown-dark ml-0.5" />}
            </button>

            {/* Right: Volume Sliders */}
            <div className="flex items-center gap-2">
              <button
                onClick={toggleMute}
                className="text-gold-base/70 hover:text-gold-bright focus:outline-none"
              >
                {isMuted ? <VolumeX className="h-4 w-4" /> : <Volume2 className="h-4 w-4" />}
              </button>
              <input
                type="range"
                min={0}
                max={1}
                step={0.05}
                value={isMuted ? 0 : volume}
                onChange={handleVolumeChange}
                className="w-16 h-1 bg-brown-light rounded-lg appearance-none cursor-pointer accent-gold-base focus:outline-none"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

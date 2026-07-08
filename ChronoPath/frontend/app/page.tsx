"use client";

import React, { useState, useEffect } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster, toast } from "sonner";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

// Screens
import LandingScreen from "../components/screens/LandingScreen";
import PermissionScreen from "../components/screens/PermissionScreen";
import JourneyScreen from "../components/screens/JourneyScreen";
import LoadingScreen from "../components/screens/LoadingScreen";
import StoryScreen from "../components/screens/StoryScreen";
import TimelineScreen from "../components/screens/TimelineScreen";
import ProfileScreen from "../components/screens/ProfileScreen";
import ErrorScreen, { ErrorType } from "../components/screens/ErrorScreen";

import { generateStory, savePlaceToJourney } from "../services/api";
import { GenerateResponse } from "../types";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function ChronoPathAppContent() {
  const [activeScreen, setActiveScreen] = useState<string>("landing");
  const [coords, setCoords] = useState<{ lat: number; lng: number } | null>(null);
  const [storyData, setStoryData] = useState<GenerateResponse | null>(null);
  
  // Error handling states
  const [errorType, setErrorType] = useState<ErrorType>("GENERATION_FAILED");
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [lastExploreOptions, setLastExploreOptions] = useState<any>(null);

  // Monitor online status
  const [isOnline, setIsOnline] = useState(true);

  useEffect(() => {
    if (typeof window !== "undefined") {
      setIsOnline(navigator.onLine);
      const handleOnline = () => setIsOnline(true);
      const handleOffline = () => setIsOnline(false);
      window.addEventListener("online", handleOnline);
      window.addEventListener("offline", handleOffline);
      return () => {
        window.removeEventListener("online", handleOnline);
        window.removeEventListener("offline", handleOffline);
      };
    }
  }, []);

  const handleStartJourney = () => {
    if (coords) {
      setActiveScreen("explore");
    } else {
      setActiveScreen("permission");
    }
  };

  const handlePermissionGranted = (userCoords: { lat: number; lng: number }) => {
    setCoords(userCoords);
    setActiveScreen("explore");
    toast.success("Location coordinates successfully acquired!");
  };

  const handlePermissionDenied = (errorMsg: string) => {
    setErrorType("LOCATION_DENIED");
    setErrorMessage(errorMsg);
    setActiveScreen("error");
  };

  const handleExplore = async (options: {
    language?: string;
    age?: number;
    origin?: string;
    background?: string;
  }) => {
    if (!isOnline) {
      setErrorType("NO_INTERNET");
      setActiveScreen("error");
      return;
    }

    if (!coords) {
      setErrorType("LOCATION_DENIED");
      setErrorMessage("No active GPS coordinates found. Please allow location access.");
      setActiveScreen("error");
      return;
    }

    setLastExploreOptions(options);
    setActiveScreen("loading");

    try {
      const response = await generateStory({
        user_id: "user-1",
        latitude: coords.lat,
        longitude: coords.lng,
        ...options,
      });

      if (!response.safe) {
        throw new Error("The AI supervisor identified unsafe/inappropriate content for this location.");
      }

      setStoryData(response);
      
      // Save spot to timeline
      const placeName = typeof response.place === "string" ? response.place : response.place.name;
      await savePlaceToJourney(placeName, response.text.title, coords.lat, coords.lng);
      
      setActiveScreen("story");
      toast.success("Chronicle generated successfully!");
    } catch (err: any) {
      console.error(err);
      
      if (err.code === "ERR_NETWORK" || !err.response) {
        setErrorType("SERVER_UNAVAILABLE");
        setErrorMessage("Could not connect to ChronoPath backend servers. Make sure your Python server is running on port 8000.");
      } else {
        setErrorType("GENERATION_FAILED");
        setErrorMessage(err.response?.data?.detail || err.message || "Failed to generate story details.");
      }
      setActiveScreen("error");
    }
  };

  const handleRetry = () => {
    if (errorType === "LOCATION_DENIED") {
      setActiveScreen("permission");
    } else if (errorType === "NO_INTERNET") {
      if (navigator.onLine) {
        setIsOnline(true);
        if (lastExploreOptions) {
          handleExplore(lastExploreOptions);
        } else {
          setActiveScreen("explore");
        }
      } else {
        toast.error("You are still offline. Please verify your connection.");
      }
    } else {
      if (lastExploreOptions) {
        handleExplore(lastExploreOptions);
      } else {
        setActiveScreen("explore");
      }
    }
  };

  const renderScreen = () => {
    switch (activeScreen) {
      case "landing":
        return <LandingScreen onStart={handleStartJourney} />;
      case "permission":
        return (
          <PermissionScreen
            onPermissionGranted={handlePermissionGranted}
            onPermissionDenied={handlePermissionDenied}
          />
        );
      case "explore":
        return (
          <JourneyScreen
            latitude={coords?.lat || 18.5196}
            longitude={coords?.lng || 73.8553}
            onExplore={handleExplore}
          />
        );
      case "loading":
        return <LoadingScreen />;
      case "story":
        return storyData ? (
          <StoryScreen data={storyData} onExploreMore={() => setActiveScreen("explore")} />
        ) : (
          <JourneyScreen
            latitude={coords?.lat || 18.5196}
            longitude={coords?.lng || 73.8553}
            onExplore={handleExplore}
          />
        );
      case "timeline":
        return <TimelineScreen />;
      case "profile":
        return <ProfileScreen />;
      case "error":
        return (
          <ErrorScreen
            type={errorType}
            message={errorMessage}
            onRetry={handleRetry}
            onBack={() => setActiveScreen("explore")}
          />
        );
      default:
        return <LandingScreen onStart={handleStartJourney} />;
    }
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar activeScreen={activeScreen} setActiveScreen={setActiveScreen} />
      <main className="flex-1 w-full max-w-6xl mx-auto px-4 sm:px-6 flex flex-col justify-center">
        {renderScreen()}
      </main>
      <Footer />
    </div>
  );
}

export default function Home() {
  return (
    <QueryClientProvider client={queryClient}>
      <ChronoPathAppContent />
      <Toaster position="top-right" richColors toastOptions={{ duration: 3000 }} />
    </QueryClientProvider>
  );
}

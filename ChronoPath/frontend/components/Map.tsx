"use client";

import React, { useState } from "react";
import { GoogleMap, useJsApiLoader, MarkerF } from "@react-google-maps/api";
import { Compass, MapPin, Loader2 } from "lucide-react";

interface MapProps {
  latitude: number;
  longitude: number;
}

// Retro parchment Google Map styling JSON
const mapStyles = [
  { elementType: "geometry", stylers: [{ color: "#ebe3cd" }] },
  { elementType: "labels.text.fill", stylers: [{ color: "#523735" }] },
  { elementType: "labels.text.stroke", stylers: [{ color: "#f5f1e6" }] },
  {
    featureType: "administrative",
    elementType: "geometry.stroke",
    stylers: [{ color: "#c9b2a6" }],
  },
  {
    featureType: "administrative.land_parcel",
    elementType: "geometry.stroke",
    stylers: [{ color: "#dcd2be" }],
  },
  {
    featureType: "administrative.land_parcel",
    elementType: "labels.text.fill",
    stylers: [{ color: "#ae9e90" }],
  },
  {
    featureType: "landscape.natural",
    elementType: "geometry",
    stylers: [{ color: "#dfd2ae" }],
  },
  {
    featureType: "poi",
    elementType: "geometry",
    stylers: [{ color: "#dfd2ae" }],
  },
  {
    featureType: "poi",
    elementType: "labels.text.fill",
    stylers: [{ color: "#93817c" }],
  },
  {
    featureType: "poi.park",
    elementType: "geometry.fill",
    stylers: [{ color: "#a5b076" }],
  },
  {
    featureType: "poi.park",
    elementType: "labels.text.fill",
    stylers: [{ color: "#447530" }],
  },
  {
    featureType: "road",
    elementType: "geometry",
    stylers: [{ color: "#f5f1e6" }],
  },
  {
    featureType: "road.arterial",
    elementType: "geometry",
    stylers: [{ color: "#fdfcf8" }],
  },
  {
    featureType: "road.highway",
    elementType: "geometry",
    stylers: [{ color: "#f8c967" }],
  },
  {
    featureType: "road.highway",
    elementType: "geometry.stroke",
    stylers: [{ color: "#e9bc62" }],
  },
  {
    featureType: "road.highway.controlled_access",
    elementType: "geometry",
    stylers: [{ color: "#e98d58" }],
  },
  {
    featureType: "road.highway.controlled_access",
    elementType: "geometry.stroke",
    stylers: [{ color: "#db8555" }],
  },
  {
    featureType: "road.local",
    elementType: "labels.text.fill",
    stylers: [{ color: "#806b63" }],
  },
  {
    featureType: "transit.line",
    elementType: "geometry",
    stylers: [{ color: "#dfd2ae" }],
  },
  {
    featureType: "transit.line",
    elementType: "labels.text.fill",
    stylers: [{ color: "#8f7d77" }],
  },
  {
    featureType: "transit.line",
    elementType: "labels.text.stroke",
    stylers: [{ color: "#ebe3cd" }],
  },
  {
    featureType: "transit.station",
    elementType: "geometry",
    stylers: [{ color: "#dfd2ae" }],
  },
  {
    featureType: "water",
    elementType: "geometry.fill",
    stylers: [{ color: "#b9d3c2" }],
  },
  {
    featureType: "water",
    elementType: "labels.text.fill",
    stylers: [{ color: "#92998d" }],
  },
];

const containerStyle = {
  width: "100%",
  height: "100%",
  borderRadius: "1rem",
};

export default function Map({ latitude, longitude }: MapProps) {
  const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || "";
  
  const { isLoaded, loadError } = useJsApiLoader({
    id: "google-map-script",
    googleMapsApiKey: apiKey,
  });

  const center = {
    lat: latitude,
    lng: longitude,
  };

  // Fallback map layout if no API key is set
  if (!apiKey || loadError) {
    return (
      <div className="relative w-full h-full min-h-[300px] bg-parchment-dark border border-gold-base/30 rounded-2xl flex flex-col items-center justify-center p-6 text-center select-none overflow-hidden">
        {/* Artistic Grid Overlay */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(197,168,128,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(197,168,128,0.1)_1px,transparent_1px)] bg-[size:24px_24px] pointer-events-none" />
        
        {/* Decorative Compass Background */}
        <div className="absolute bottom-4 right-4 text-gold-dark/15 opacity-40 pointer-events-none">
          <Compass className="h-40 w-40 animate-spin-slow" />
        </div>

        {/* Dynamic Location Marker Pin on Fallback Canvas */}
        <div className="relative z-10 flex flex-col items-center gap-3">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-brown-base/10 border border-gold-base/50 shadow-inner">
            <MapPin className="h-8 w-8 text-gold-dark animate-bounce" />
          </div>
          <div>
            <h3 className="font-serif text-lg font-bold text-brown-dark">Historical Compass</h3>
            <p className="text-xs text-brown-light/70 font-mono mt-1">
              Lat: {latitude.toFixed(6)} | Lng: {longitude.toFixed(6)}
            </p>
            <div className="mt-4 px-3 py-1 rounded bg-gold-base/10 border border-gold-base/20 inline-block text-[11px] font-medium text-gold-dark">
              {!apiKey ? "Operating in Historical Map Preview Mode" : "Google Maps initialization failed; falling back"}
            </div>
          </div>
        </div>

        {/* Small subtle compass details */}
        <div className="absolute top-4 left-4 text-[10px] font-mono text-brown-light/40 flex flex-col text-left">
          <span>N 18° 31' 10.56"</span>
          <span>E 73° 51' 19.08"</span>
        </div>
      </div>
    );
  }

  if (!isLoaded) {
    return (
      <div className="w-full h-full min-h-[300px] bg-parchment-base border border-parchment-dark rounded-2xl flex items-center justify-center">
        <Loader2 className="h-8 w-8 text-gold-dark animate-spin" />
      </div>
    );
  }

  return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={15}
      options={{
        styles: mapStyles,
        disableDefaultUI: true,
        zoomControl: true,
      }}
    >
      <MarkerF position={center} />
    </GoogleMap>
  );
}

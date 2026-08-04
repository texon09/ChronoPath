"use client";

import React from "react";
import { Compass, History, User, MapPin } from "lucide-react";

interface NavbarProps {
  activeScreen: string;
  setActiveScreen: (screen: string) => void;
  user?: any;
}

export default function Navbar({ activeScreen, setActiveScreen, user }: NavbarProps) {
  const navItems = [
    { id: "explore", label: "Explore", icon: Compass },
    { id: "timeline", label: "Timeline", icon: History },
    { id: "profile", label: "Profile", icon: User },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b border-parchment-dark bg-parchment-light/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
        {/* Brand logo & title */}
        <button
          onClick={() => setActiveScreen("landing")}
          className="flex items-center gap-2 text-left focus:outline-none group"
        >
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-brown-base text-gold-base shadow-md transition-all duration-300 group-hover:bg-brown-light group-hover:text-gold-bright">
            <Compass className="h-5 w-5 animate-spin-slow" />
          </div>
          <div>
            <h1 className="font-serif text-lg font-bold tracking-tight text-brown-dark sm:text-xl">
              Nomad Notes <span className="text-gold-dark">AI</span>
            </h1>
            <span className="text-[10px] uppercase tracking-wider text-brown-light/70 font-semibold block -mt-1">
              Historical Multimodal Explorer
            </span>
          </div>
        </button>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeScreen === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveScreen(item.id)}
                className={`flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium transition-all duration-300 focus:outline-none ${
                  isActive
                    ? "bg-brown-base text-gold-base shadow-sm"
                    : "text-brown-light hover:bg-parchment-dark/50 hover:text-brown-dark"
                }`}
              >
                <Icon className="h-4 w-4" />
                {item.label}
              </button>
            );
          })}
          
          {/* Logout Button */}
          {user && (
            <button
              onClick={() => {
                import("../services/firebase").then(({ auth }) => {
                  auth.signOut();
                  setActiveScreen("landing");
                });
              }}
              className="flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium text-red-700/80 hover:bg-red-900/10 hover:text-red-900 transition-all duration-300 focus:outline-none ml-2"
            >
              Log Out
            </button>
          )}
        </nav>

        {/* Mobile Navigation icons */}
        <nav className="flex md:hidden items-center gap-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeScreen === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveScreen(item.id)}
                title={item.label}
                className={`flex h-10 w-10 items-center justify-center rounded-lg transition-all duration-300 focus:outline-none ${
                  isActive
                    ? "bg-brown-base text-gold-base shadow-sm"
                    : "text-brown-light hover:bg-parchment-dark/50 hover:text-brown-dark"
                }`}
              >
                <Icon className="h-5 w-5" />
              </button>
            );
          })}
          
          {/* Mobile Logout */}
          {user && (
            <button
              onClick={() => {
                import("../services/firebase").then(({ auth }) => {
                  auth.signOut();
                  setActiveScreen("landing");
                });
              }}
              title="Log Out"
              className="flex h-10 w-10 items-center justify-center rounded-lg transition-all duration-300 focus:outline-none text-red-700/80 hover:bg-red-900/10 hover:text-red-900 ml-1"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
            </button>
          )}
        </nav>
      </div>
    </header>
  );
}

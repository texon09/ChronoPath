export interface GenerateRequest {
  user_id: string;
  latitude: number;
  longitude: number;
  language?: string;
  age?: number;
  origin?: string;
  background?: string;
  name?: string;
}

export interface PlaceResponse {
  id: string;
  name: string;
}

export interface TextResponse {
  title: string;
  story: string;
}

export interface AudioResponse {
  url: string;
  duration: string;
}

export interface VisualResponse {
  url: string;
}

export interface MetaResponse {
  latency_ms: string;
  cache_hit: string;
}

export interface GenerateResponse {
  request_id: string;
  place: PlaceResponse | string;
  text: TextResponse;
  audio?: AudioResponse | null;
  visual?: VisualResponse | null;
  safe: boolean;
  meta?: MetaResponse | null;
}

export interface Place {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
  timestamp: string;
  storyTitle: string;
}

export interface Journey {
  id: string;
  date: string;
  places: Place[];
}

export interface Profile {
  preferredLanguage: string;
  storiesViewedCount: number;
  placesVisitedCount: number;
  recentJourney?: Journey;
  age?: number;
  origin?: string;
  background?: string;
  name?: string;
}

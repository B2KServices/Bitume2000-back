import { Request, Response } from "express";
import * as console from "node:console";
import config from "@/src/configs/config";

export const getNextBus = async (req: Request, res: Response) => {
  const stopId = req.query.stopId;
  console.log(`Fetching next bus for stop ID: ${stopId}`);
  const url = `https://external.transitapp.com/v3/public/stop_departures?global_stop_id=${stopId}`;
  const apiKey = config.TRANSIT_API_KEY || "";
  try {
    const resp = await fetch(url, {
      headers: { Accept: "application/json", apiKey: apiKey },
    });
    const data = await resp.json();
    res.json(data);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to fetch Transit API" });
  }
};

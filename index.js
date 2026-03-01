const express = require('express');
const axios = require('axios');
const { DateTime } = require('luxon');

const app = express();
const PORT = process.env.PORT || 3000;
const OWNER_NAME = "@A_4owner";

// 🔑 Multiple Keys Database
const KEYS_DB = {
  "ZEXX@_4M": { expiry: "2027-12-31", status: "Premium" },
  "OWNER_TEST": { expiry: "2032-12-30", status: "Trial" },
  "ZEXX_1M": { expiry: "2026-08-15", status: "Basic" },
  "ZEXX_T4L": { expiry: "2026-03-21", status: "Premium" }
};

app.use(express.json());

app.get('/search', async (req, res) => {
  const { key, rc } = req.query;

  // 🔐 Key Check
  if (!key || !KEYS_DB[key]) {
    return res.status(401).json({
      success: false,
      type: "error",
      error: "Invalid Key!",
      owner: OWNER_NAME
    });
  }

  // 📅 Expiry Check
  const today = DateTime.local();
  const expiryDate = DateTime.fromISO(KEYS_DB[key].expiry);

  if (today > expiryDate) {
    return res.status(403).json({
      success: false,
      type: "error",
      error: "Key Expired!",
      owner: OWNER_NAME
    });
  }

  // 🚗 RC Check
  if (!rc) {
    return res.status(400).json({
      success: false,
      type: "error",
      error: "rc parameter required",
      owner: OWNER_NAME
    });
  }

  try {
    // 🔥 NEW VEHICLE RC API CALL
    const response = await axios.get(
      "https://akash-vehicle-to-number-api.vercel.app/",
      {
        params: {
          rc: rc,
          key: "AKASH_PARMA"
        },
        timeout: 15000
      }
    );

    let apiData = response.data || {};

    // 🔁 Branding Replace
    apiData.branding = "@A_4owner";
    apiData.developer = "@A_4owner";
    apiData.join = "@cyber_osint_v4_bot";
    apiData.key_info = {
      owner: "OWNER"
    };

    return res.json({
      success: true,
      type: "success",
      owner: OWNER_NAME,
      data: apiData
    });

  } catch (error) {
    return res.status(504).json({
      success: false,
      type: "error",
      error: "External API Timeout / Network Issue",
      details: error.message,
      owner: OWNER_NAME
    });
  }
});

app.get('/', (req, res) => {
  res.json({
    success: true,
    type: "success",
    message: "API Running Successfully 🚀",
    owner: OWNER_NAME
  });
});

module.exports = app;

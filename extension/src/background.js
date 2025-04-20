const aitutorUrl = process.env.REQUEST_URL;
const aitutorDomain = process.env.DOMAIN;
const apiKey = process.env.API_KEY;
const apiKeyName = process.env.API_KEY_NAME;

// if (typeof browser === "undefined") {
//   // firefox
//   // var browser = chrome;
//   console.log("idk");
// } else {
//   // chrome
//   chrome.sidePanel
//     .setPanelBehavior({ openPanelOnActionClick: true })
//     .catch((error) => console.error(error));
// }

chrome.sidePanel
  .setPanelBehavior({ openPanelOnActionClick: true })
  .catch((error) => console.error(error));

const isFirefox = typeof browser !== "undefined" && browser.sidebarAction;
const isChrome = typeof chrome !== "undefined" && !isFirefox;

async function getData(url) {
  let response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  });
  let resp = await response.json();
  return resp;
}

async function postData(url, data) {
  let response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "AITUTOR-API-KEY": apiKey,
      Accept: "application/json",
    },
    body: JSON.stringify(data),
  });
  let resp = await response.json();
  return resp;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "sendCourse") {
    postData(`${aitutorUrl}course`, message.data);
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "sendUser") {
    postData(`${aitutorUrl}user`, message.data);
  }
});

chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  if (message.type === "setCookie") {
    token_data = await postData(`${aitutorUrl}token`, message.data);

    chrome.cookies.set(
      // TODO: Add another cookie to `https://beta.aitutor.live`
      {
        url: aitutorDomain,
        name: "token",
        value: token_data.token,
        expirationDate: Math.floor(Date.now() / 1000) + 86400, // 3600, // Expires in 1 hour
        // NOTE: 86400 - 1 day
        sameSite: "no_restriction", // SameSite=None
        secure: true, // Secure attribute // only https
      },
      () => {
        console.log(`Cookie set for aitutor.live: ${message.data}`);
      },
    );
  }
});

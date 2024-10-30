const domain = window.location.origin;
const current_page = window.location.pathname;
const institution = window.location.hostname.split(".")[0];
const aitutorUrl = process.env.REQUEST_URL;
const apiKey = process.env.API_KEY;
const apiKeyName = process.env.API_KEY_NAME;

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
      "AITUTOR-API-KEY": "",
      Accept: "application/json",
    },
    body: JSON.stringify(data),
  });
  let resp = await response.json();
  return resp;
}

async function dostuff() {
  let data = await getData(`${domain}/api/v1/users/self`);

  let resp = await postData(`${aitutorUrl}v1/ingest`, {
    institution: institution,
    canvas_id: data.id,
    first_name: data.first_name,
    last_name: data.last_name,
    // effective_local: data.effective_local,
    avatar_url: data.avatar_url,
  });
}

dostuff();

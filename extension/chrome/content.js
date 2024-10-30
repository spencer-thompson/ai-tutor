const domain = window.location.origin;
// const aitutor_url = "http";

async function getData(url) {
  let response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  });
  let data = await response.json();
  return data;
}

async function postData(url, data) {
  let response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "AITUTOR-API-KEY": "",
      Accept: "application/json",
    },
    body: JSON.stringify(data),
  });
  let data = await response.json();
  return data;
}

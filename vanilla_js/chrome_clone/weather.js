const weather = document.querySelector(".js-weather");

const API_KEY = "a61e941aa2a06c63912dc57f90514ff0";
const COORDS = 'coords';

function getWeather(lat, lon) {
  // fetch를 기다렸다가 수행해야하는 함수가 있으면
  // 아래와 같이 then 설정
  // 따로 설정 시 fetch를 기다리지 않고 수행하여, 문제가 생길 수 있음
  fetch(
    `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`
  ).then(function(response) {
    // 여기서 then을 끝내버리면, json이 불러와질때까지 기다리게됨
    // 아래에 then을 더 붙여줌으로써 json이 다 불러와졌을때 이후의
    // 동작을 설계할 수 있게 됨 -> 아직 정확히 이해는 안 되지만, 로직 봐두자.
    return response.json();
  }).then(function(json) {
    const temperature = json.main.temp;
    const place = json.name;
    weather.innerText = `${temperature} @ ${place}`;
  });
}

function saveCoords(coordsObj) {
  localStorage.setItem(COORDS, JSON.stringify(coordsObj));
}

function handleGeoSuccess(position) {
  const latitude = position.coords.latitude;
  const longitude = position.coords.longitude;
  const coordsObj = {
    latitude,
    longitude,
  };
  saveCoords(coordsObj);
  getWeather(latitude, longitude);
}

function handleGeoError() {
  console.log("Cant access geo location");
}

function askForCoords() {
  // navigator 말고도 window, document 등 많은 API 존재
  navigator.geolocation.getCurrentPosition(handleGeoSuccess, handleGeoError);
}

function loadCoords() {
  const loadedCoords = localStorage.getItem(COORDS);
  if (loadedCoords === null) {
    askForCoords();
  } else {
    const parseCoords = JSON.parse(loadedCoords);
    getWeather(parseCoords.latitude, parseCoords.longitude);
  }
}

function init() {
  loadCoords();
}

init();
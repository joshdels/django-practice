let map = L.map('map', {
  zoomControl: false
}).setView([13.41, 122.56], 5);

var myFAIcon = L.divIcon({
    html: '<i class="fas fa-map-pin fa-3x" style="color: red;"></i>',
    iconSize: [25, 41],   // approximate marker size
    iconAnchor: [12, 41], // point of the icon which will correspond to marker's location
    popupAnchor: [0, -40], // where the popup will open relative to the iconAnchor
    className: 'my-fa-icon' // optional class to style further
});

let myLocation = L.marker(
  [7.442619, 125.804142], 
  {icon: myFAIcon}
).addTo(map);

myLocation.bindPopup(`
  <div style="line-height: 1.4; font-size: 14px;">
    <h5 style="margin: 0 0 8px;">🏠 My Hometown</h5>
    <p style="margin: 4px 0;">
      <i class="fas fa-tree" style="color: green;"></i> Peaceful rural-style city<br>
      <i class="fas fa-wallet" style="color: #5bc0de;"></i> Low cost of living<br>
      <i class="fas fa-coffee" style="color: #795548;"></i> I'm open for a coffee talk!
    </p>
  </div>
`).openPopup();

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 11,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
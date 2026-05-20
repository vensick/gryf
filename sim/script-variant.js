const variants = ['A','B','C','D'];
const cycleStartUTC = Date.UTC(1970,0,1,8); // cykl startuje 08:00 UTC
const cycleHours = 48; // długość wariantu w godzinach
const step = 0.1; // krok skali w tabeli
// ------------------------------------------------

// Funkcja aktualizująca zegar GMT
function updateGMT() {
  const now = new Date();
  document.getElementById('gmtTime').textContent = now.toISOString().slice(0,19).replace('T',' ');
}

// Funkcja licząca czas do końca wariantu
function timeToNextVariant() {
  const now = new Date();
  const hoursSinceStart = (now.getTime() - cycleStartUTC)/(1000*60*60);
  const hoursIntoCurrent = hoursSinceStart % cycleHours;
  const remainingHours = cycleHours - hoursIntoCurrent;

  const h = Math.floor(remainingHours);
  const m = Math.floor((remainingHours - h) * 60);
  return `${h}h ${m}min`;
}

// Funkcja zwracająca aktualny wariant
function getCurrentVariant() {
  const nowUTC = new Date().getTime();
  const hoursSinceStart = (nowUTC - cycleStartUTC)/(1000*60*60);
  const index = Math.floor(hoursSinceStart / cycleHours) % variants.length;
  return variants[index];
}

// Dekodowanie szyfru BR
function decodeBRcodes(codeString){
  const brs=[];
  for(let i=0;i<codeString.length;i+=3){
    const code = codeString.slice(i,i+3);
    const num = parseInt(code,10);
    brs.push(isNaN(num)?null:num/10);
  }
  return brs;
}

// Renderowanie tabeli pionowej dla jednego wariantu
function renderVariantScale(variant){
  const tbody = document.querySelector('#variantScale tbody');
  tbody.innerHTML='';

  const values = decodeBRcodes(variantBRcodes[variant]);
  const numericValues = values.filter(v=>v!==null);
  const maxValue = Math.ceil(Math.max(...numericValues)*10)/10;

  document.getElementById('variantCode').textContent = variant;

  for(let i=1.0;i<=maxValue+0.001;i+=step){
    const tr = document.createElement('tr');
    const tdScale = document.createElement('td');
    tdScale.textContent = i.toFixed(1);
    const tdMark = document.createElement('td');

    if(values.some(v=>v!==null && Math.abs(v - parseFloat(i.toFixed(1))) < 0.001)){
      tdMark.textContent = 'x';
    }

    tr.appendChild(tdScale);
    tr.appendChild(tdMark);
    tbody.appendChild(tr);
  }
}

// Funkcja aktualizująca wszystko co sekundę
function updateAll(){
  updateGMT();
  document.getElementById('timeLeft').textContent = timeToNextVariant();
  renderVariantScale(getCurrentVariant());
}

// Uruchomienie
updateAll();
setInterval(updateAll,1000);

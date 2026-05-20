

function highlightBRs(threshold) {
  document.querySelectorAll('#brTable td').forEach(td => {
    const val = parseFloat(td.textContent);
    if (!isNaN(val)) {

      // BR mniejsze
      if (val < threshold) {
        td.style.backgroundColor = '#2a0f0f';
        td.style.color = '#ff4444';
        td.style.fontWeight = 'bold';

      // BR równe
      } else if (val === threshold) {
        td.style.backgroundColor = '#066';
        td.style.color = '#6ff';
        td.style.fontWeight = 'bold';

      // BR większe
      } else {
        td.style.backgroundColor = '';
        td.style.color = '';
        td.style.fontWeight = '';
      }
    }
  });
}



document.getElementById('brInput').addEventListener('input', () => {
  const input = document.getElementById('brInput').value.trim();
  const br = parseFloat(input);
  if (!isNaN(br)) {
    highlightBRs(br);
  }
});

const variants = ['A','B','C','D'];
const cycleStartUTC = Date.UTC(1970,0,1,8);
const cycleHours = 48;


function updateGMT() {
  const now = new Date();
  document.getElementById('gmtTime').textContent = now.toISOString().slice(0,19).replace('T',' ');
}

function timeToNextVariant() {
  const now = new Date();
  const hoursSinceStart = (now.getTime() - cycleStartUTC) / (1000*60*60);
  const hoursIntoCurrent = hoursSinceStart % cycleHours;
  const remainingHours = cycleHours - hoursIntoCurrent;

  const h = Math.floor(remainingHours);
  const m = Math.floor((remainingHours - h) * 60);

  let result = '';
  if(h>0) result += `${h}h `;
  result += `${m}min`;
  return result;
}

function getVariantForDate(date) {
  const nowUTC = date.getTime();
  const hours = Math.floor((nowUTC - cycleStartUTC) / (1000*60*60));
  const index = Math.floor(hours / cycleHours) % variants.length;
  return variants[index];
}

function decodeBRcodes(codeString) {
  const brs = [];
  for(let i=0;i<codeString.length;i+=3){
    const code = codeString.slice(i,i+3);
    const num = parseInt(code,10);
    if(isNaN(num)){
      brs.push('');
    } else {
      brs.push((num/10).toFixed(1));
    }
  }
  return brs;
}

function renderBRTable() {
  const tbody = document.querySelector('#brTable tbody');
  const rows = [];
  variants.forEach(variant => {
    const brs = decodeBRcodes(variantBRcodes[variant]);
    brs.forEach((br,rowIndex)=>{
      if(!rows[rowIndex]) rows[rowIndex] = document.createElement('tr');
      const td = document.createElement('td');
      td.textContent = br;
      rows[rowIndex].appendChild(td);
    });
  });
  rows.forEach(row=>tbody.appendChild(row));
}

function highlightColumn(variant) {
  const index = { A:0,B:1,C:2,D:3 }[variant];
  document.getElementById('variantCode').textContent = variant;

  const table = document.getElementById('brTable');
  table.querySelectorAll('thead th').forEach((th,i)=>th.classList.toggle('active', i===index));
  table.querySelectorAll('tbody tr').forEach(row=>{
    row.querySelectorAll('td').forEach((td,i)=>td.classList.toggle('active', i===index));
  });
}

function updateAll() {
  updateGMT();
  document.getElementById('timeLeft').textContent = timeToNextVariant();
  highlightColumn(getVariantForDate(new Date()));
}

renderBRTable();
updateAll();
setInterval(updateAll,1000);
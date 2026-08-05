const state={capabilities:null};
const form=document.querySelector('#search-form');
const filters=document.querySelector('#filters');
const template=document.querySelector('#filter-template');
const statusNode=document.querySelector('#status');
const resultsNode=document.querySelector('#results');
const emptyNode=document.querySelector('#empty-state');
const searchButton=document.querySelector('#search-button');

function addFilter(initial={field:'displayName',operator:'eq',value:''}){
  const fragment=template.content.cloneNode(true);
  const row=fragment.querySelector('.filter-row');
  row.querySelector('.filter-field').value=initial.field;
  row.querySelector('.filter-operator').value=initial.operator;
  row.querySelector('.filter-value').value=initial.value;
  row.querySelector('.remove-filter').addEventListener('click',()=>row.remove());
  filters.appendChild(fragment);
}

function coerceValue(field,raw){
  if(field==='scope'&&raw.trim()!==''){
    const value=Number(raw);
    if(Number.isNaN(value)) throw new Error('Scope must be numeric.');
    return value;
  }
  return raw;
}

function payload(){
  return {
    root:document.querySelector('#root').value||null,
    filters:[...filters.querySelectorAll('.filter-row')]
      .map(row=>{
        const field=row.querySelector('.filter-field').value;
        const raw=row.querySelector('.filter-value').value.trim();
        return {field,operator:row.querySelector('.filter-operator').value,value:coerceValue(field,raw)};
      })
      .filter(item=>item.value!==''),
    limit:Number(document.querySelector('#limit').value)
  };
}

function renderResults(data,elapsed){
  resultsNode.replaceChildren();
  const items=data.results||[];
  for(const item of items){
    const row=document.createElement('tr');
    row.tabIndex=0;
    row.dataset.root=item.root;
    row.dataset.classname=item.classname;
    for(const value of [item.displayName||'—',item.classname,item.root,item.parent||'—']){
      const cell=document.createElement('td');cell.textContent=value;row.appendChild(cell);
    }
    resultsNode.appendChild(row);
  }
  emptyNode.hidden=items.length>0;
  emptyNode.textContent=items.length?'':items.length===0?'No results.':'';
  statusNode.textContent=`${items.length} result${items.length===1?'':'s'} · ${elapsed.toFixed(0)} ms`;
}

async function loadCapabilities(){
  const response=await fetch('/api/capabilities');
  const body=await response.json();
  if(!response.ok||body.status!=='ok') throw new Error(body?.error?.message||'Unable to load capabilities.');
  state.capabilities=body.data;
  const root=document.querySelector('#root');
  root.replaceChildren();
  for(const name of body.data.snapshot.roots){
    const option=document.createElement('option');option.value=name;option.textContent=name;root.appendChild(option);
  }
  document.querySelector('#dataset-summary').textContent=`${body.data.snapshot.presetLabel} · ${body.data.snapshot.gameVersion}`;
}

form.addEventListener('submit',async event=>{
  event.preventDefault();searchButton.disabled=true;statusNode.textContent='Searching…';
  const started=performance.now();
  try{
    const response=await fetch('/api/basic',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload())});
    const body=await response.json();
    if(!response.ok||body.status!=='ok') throw new Error(body?.error?.message||`Request failed (${response.status}).`);
    renderResults(body.data,performance.now()-started);
  }catch(error){resultsNode.replaceChildren();emptyNode.hidden=false;emptyNode.textContent='Search failed.';statusNode.textContent=error.message||String(error);}
  finally{searchButton.disabled=false;}
});

document.querySelector('#add-filter').addEventListener('click',()=>addFilter());
document.querySelector('#reset-button').addEventListener('click',()=>{
  form.reset();filters.replaceChildren();addFilter();resultsNode.replaceChildren();emptyNode.hidden=false;emptyNode.textContent='Run a search to display results.';statusNode.textContent='Ready.';
});

addFilter();
loadCapabilities().catch(error=>{statusNode.textContent=error.message||String(error);});

const canvas = new fabric.Canvas('canvas');
let blockTypes = {};
let totalCost = 0;

fetch('/api/block-types/')
  .then(res => res.json())
  .then(data => {
    data.forEach(block => blockTypes[block.name] = block);
    addBlock('Laboratory');  // Default add
  });

canvas.on('object:modified', updateTotalCost);
canvas.on('object:added', updateTotalCost);

function updateTotalCost() {
    totalCost = 0;
    canvas.getObjects().forEach(obj => {
        const block = blockTypes[obj.blockType];
        if (block) {
            const area = (obj.width * obj.scaleX) * (obj.height * obj.scaleY);
            totalCost += area * parseFloat(block.price_per_sqft);
        }
    });
    document.getElementById('total-cost').innerText = totalCost.toFixed(2);
}

function addBlock(type) {
    const rect = new fabric.Rect({
        left: 100,
        top: 100,
        fill: 'skyblue',
        width: 100,
        height: 100,
        blockType: type,
        hasControls: true,
    });
    canvas.add(rect);
}

function saveDesign() {
    const projectName = prompt("Enter project name:");
    const blocks = canvas.getObjects().map(obj => ({
        block_type: Object.values(blockTypes).find(bt => bt.name === obj.blockType).id,
        length: obj.width * obj.scaleX,
        width: obj.height * obj.scaleY,
        x: obj.left,
        y: obj.top
    }));

    fetch('/api/save-project/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ name: projectName, blocks })
    })
    .then(res => res.json())
    .then(data => alert(data.message || 'Saved!'));
}

function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        if (cookie.trim().startsWith(name + '=')) {
            return decodeURIComponent(cookie.trim().substring(name.length + 1));
        }
    }
    return '';
}

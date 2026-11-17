const fs = require('fs'), path = require('path'), pcbStackup = require('pcb-stackup');
const dir = process.argv[2], out = process.argv[3];
const files = fs.readdirSync(dir).filter(f => !/In\d_Cu/.test(f)).map(f => ({ filename: f, gerber: fs.createReadStream(path.join(dir, f)) }));
pcbStackup(files, { color: { fr4: '#4a4a2a', cu: '#c8a040', cf: '#e8c040', sm: 'rgba(20,70,30,0.82)', ss: '#f0f0f0', sp: '#a8a8a8', out: '#000' } }).then(s => {
  fs.writeFileSync(out + '_top.svg', s.top.svg); fs.writeFileSync(out + '_bottom.svg', s.bottom.svg); console.log('ok');
});

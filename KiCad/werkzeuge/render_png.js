const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1376, height: 1376 } });
  for (const [i, o] of [[process.argv[2] + '_top.svg', process.argv[3] + '/render_top.png'], [process.argv[2] + '_bottom.svg', process.argv[3] + '/render_bottom.png']]) {
    let s = fs.readFileSync(i, 'utf8').replace(/width="[^"]*" height="[^"]*"/, 'width="1336" height="1336"');
    await p.setContent(`<html><body style="margin:0;background:#fff;display:flex;align-items:center;justify-content:center;height:1376px">${s}</body></html>`);
    await p.screenshot({ path: o, omitBackground: true });
  }
  await b.close();
})();

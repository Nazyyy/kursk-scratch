
const puppeteer = require("puppeteer");

(async () => {
    const browser = await puppeteer.launch({
        executablePath: "/usr/bin/chromium",
        headless: true,
        args: [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--use-gl=angle",
            "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader",
            "--ignore-gpu-blocklist",
            "--disable-gpu-sandbox"
        ]
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 480, height: 360 });

    page.on("console", msg => console.log("PAGE_LOG:", msg.text()));

    await page.goto("file:///home/dima/Projects/hackathon/inspect_game/runner.html", { waitUntil: "networkidle0", timeout: 60000 });
    await page.waitForFunction(() => window.isReady === true, { timeout: 15000 });
    await new Promise(r => setTimeout(r, 1000));
    await page.screenshot({ path: "/home/dima/Projects/hackathon/inspect_game/screen_0_title.png" });
    console.log("Saved screen_0_title.png");

    // Intro / Level 1
    await page.evaluate(() => window.broadcast("start_intro"));
    await new Promise(r => setTimeout(r, 3000));
    await page.screenshot({ path: "/home/dima/Projects/hackathon/inspect_game/screen_1_intro.png" });
    console.log("Saved screen_1_intro.png");

    await page.evaluate(() => window.broadcast("goto_level1"));
    await new Promise(r => setTimeout(r, 1000));
    await page.evaluate(() => window.broadcast("start_level1_game"));
    await new Promise(r => setTimeout(r, 2000));
    await page.screenshot({ path: "/home/dima/Projects/hackathon/inspect_game/screen_1_semenov_game.png" });
    console.log("Saved screen_1_semenov_game.png");

    // Level 2
    await page.evaluate(() => window.broadcast("goto_level2"));
    await new Promise(r => setTimeout(r, 1000));
    await page.evaluate(() => window.broadcast("start_level2_game"));
    await new Promise(r => setTimeout(r, 2000));
    await page.screenshot({ path: "/home/dima/Projects/hackathon/inspect_game/screen_2_ufimtsev_game.png" });
    console.log("Saved screen_2_ufimtsev_game.png");

    // Level 3
    await page.evaluate(() => window.broadcast("goto_level3"));
    await new Promise(r => setTimeout(r, 1000));
    await page.evaluate(() => window.broadcast("start_level3_game"));
    await new Promise(r => setTimeout(r, 2000));
    await page.screenshot({ path: "/home/dima/Projects/hackathon/inspect_game/screen_3_kma_game.png" });
    console.log("Saved screen_3_kma_game.png");

    // Quiz
    await page.evaluate(() => window.broadcast("goto_hall_quiz"));
    await new Promise(r => setTimeout(r, 1000));
    await page.evaluate(() => window.broadcast("start_quiz_game"));
    await new Promise(r => setTimeout(r, 2000));
    await page.screenshot({ path: "/home/dima/Projects/hackathon/inspect_game/screen_4_quiz.png" });
    console.log("Saved screen_4_quiz.png");

    // Victory
    await page.evaluate(() => window.broadcast("show_victory"));
    await new Promise(r => setTimeout(r, 2000));
    await page.screenshot({ path: "/home/dima/Projects/hackathon/inspect_game/screen_5_victory.png" });
    console.log("Saved screen_5_victory.png");

    await browser.close();
    console.log("DONE CAPTURING!");
})().catch(e => {
    console.error("FAIL:", e);
    process.exit(1);
});

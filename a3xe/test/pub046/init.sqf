/*
    A3XE PUB046 controlled real-Arma-3 test launcher.

    Copy the a3xe folder into a test mission, start the mission, then execute:
        [] execVM "a3xe\test\pub046\init.sqf";

    Expected RPT markers:
        A3XE_PUB046=START
        A3XE_SQF_EXPORT=PASS ...
        A3XE_PUB046=WAITING_FOR_CLIPBOARD
*/

diag_log "A3XE_PUB046=START BUILD=PUB046";

private _script = "a3xe\sqf\fn_extractControlledRoot.sqf";
if !(fileExists _script) exitWith {
    diag_log format ["A3XE_PUB046=FAIL CODE=MISSING_SCRIPT PATH=%1", _script];
    hint "A3XE PUB046 failed: extractor script missing.";
};

hint "A3XE PUB046 started. Wait for the completion hint, then paste the clipboard into capture.json.";

private _handle = ["CfgWeapons", 100] execVM _script;
waitUntil {scriptDone _handle};

diag_log "A3XE_PUB046=WAITING_FOR_CLIPBOARD";
hint "A3XE PUB046 finished. The JSON capture is in the clipboard.";

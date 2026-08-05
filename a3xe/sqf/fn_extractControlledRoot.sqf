/*
    A3XE PUB039 controlled extraction prototype.

    Usage from the debug console:
        ["CfgWeapons", 100] execVM "a3xe\sqf\fn_extractControlledRoot.sqf";

    The script writes one JSON capture to the clipboard and mirrors a short
    completion marker to the RPT. It intentionally extracts only direct child
    classes and a small allow-list of scalar properties.
*/
params [
    ["_rootName", "CfgWeapons", [""]],
    ["_maxClasses", 100, [0]]
];

private _supportedRoots = ["CfgWeapons"];
if !(_rootName in _supportedRoots) exitWith {
    diag_log format ["A3XE_SQF_EXPORT=REJECTED ROOT=%1", _rootName];
};

private _fnc_escapeJson = {
    params [["_value", "", [""]]];
    private _result = "";
    {
        _result = _result + switch (_x) do {
            case 34: {"\""};
            case 92: {"\\"};
            case 10: {"\n"};
            case 13: {"\r"};
            case 9: {"\t"};
            default {toString [_x]};
        };
    } forEach toArray _value;
    _result
};

private _fnc_jsonString = {
    params ["_value"];
    format ["\"%1\"", [str _value select [1, (count str _value) - 2]] call _fnc_escapeJson]
};

private _root = configFile >> _rootName;
private _classes = ("true" configClasses _root) select {isClass _x};
_classes = [_classes, [], {configName _x}, "ASCEND"] call BIS_fnc_sortBy;
if (_maxClasses > 0 && {count _classes > _maxClasses}) then {
    _classes resize _maxClasses;
};

private _classJson = [];
{
    private _cfg = _x;
    private _classname = configName _cfg;
    private _parentCfg = inheritsFrom _cfg;
    private _parent = if (isNull _parentCfg || {_parentCfg isEqualTo _root}) then {nil} else {configName _parentCfg};

    private _properties = [];
    if (isText (_cfg >> "displayName")) then {
        _properties pushBack format ["\"displayName\":%1", [getText (_cfg >> "displayName")] call _fnc_jsonString];
    };
    if (isNumber (_cfg >> "scope")) then {
        _properties pushBack format ["\"scope\":%1", getNumber (_cfg >> "scope")];
    };
    if (isText (_cfg >> "author")) then {
        _properties pushBack format ["\"author\":%1", [getText (_cfg >> "author")] call _fnc_jsonString];
    };
    if (isText (_cfg >> "dlc")) then {
        _properties pushBack format ["\"dlc\":%1", [getText (_cfg >> "dlc")] call _fnc_jsonString];
    };

    private _parentJson = if (isNil "_parent") then {"null"} else {[_parent] call _fnc_jsonString};
    _classJson pushBack format [
        "{\"classname\":%1,\"parent\":%2,\"properties\":{%3}}",
        [_classname] call _fnc_jsonString,
        _parentJson,
        _properties joinString ","
    ];
} forEach _classes;

private _productVersion = productVersion;
private _capture = format [
    "{\"captureVersion\":\"0.1\",\"source\":\"arma3_sqf\",\"artificial\":false,\"root\":%1,\"game\":{\"product\":%2,\"version\":%3,\"build\":%4},\"selection\":{\"maxClasses\":%5,\"propertyAllowList\":[\"displayName\",\"scope\",\"author\",\"dlc\"]},\"classes\":[%6]}",
    [_rootName] call _fnc_jsonString,
    [_productVersion select 0] call _fnc_jsonString,
    [_productVersion select 2] call _fnc_jsonString,
    [_productVersion select 3] call _fnc_jsonString,
    _maxClasses,
    _classJson joinString ","
];

copyToClipboard _capture;
diag_log format ["A3XE_SQF_EXPORT=PASS ROOT=%1 CLASSES=%2 BYTES=%3", _rootName, count _classes, count _capture];

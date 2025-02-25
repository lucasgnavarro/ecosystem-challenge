# -*- coding: utf-8 -*-

enterprise_attack_pattern = {
    "type":
    "bundle",
    "id":
    "bundle--c81e3e34-4b53-4795-9c80-b07d8340d8d5",
    "spec_version":
    "2.0",
    "some_nested": {
        'some_nested_child': "it works"
    },
    "objects": [{
        "x_mitre_data_sources": [
            "Windows Registry", "Services", "Windows event logs",
            "Process command-line parameters", "Process monitoring"
        ],
        "x_mitre_permissions_required":
        ["Administrator", "root", "SYSTEM", "User"],
        "name":
        "Inhibit System Recovery",
        "description":
        "Adversaries may delete or remove built-in operating system data and turn off services designed to aid in the recovery of a corrupted system to prevent recovery.(Citation: Talos Olympic Destroyer 2018)(Citation: FireEye WannaCry 2017) Operating systems may contain features that can help fix corrupted systems, such as a backup catalog, volume shadow copies, and automatic repair features. Adversaries may disable or delete system recovery features to augment the effects of [Data Destruction](https://attack.mitre.org/techniques/T1485) and [Data Encrypted for Impact](https://attack.mitre.org/techniques/T1486).(Citation: Talos Olympic Destroyer 2018)(Citation: FireEye WannaCry 2017)\n\nA number of native Windows utilities have been used by adversaries to disable or delete system recovery features:\n\n* <code>vssadmin.exe</code> can be used to delete all volume shadow copies on a system - <code>vssadmin.exe delete shadows /all /quiet</code>\n* [Windows Management Instrumentation](https://attack.mitre.org/techniques/T1047) can be used to delete volume shadow copies - <code>wmic shadowcopy delete</code>\n* <code>wbadmin.exe</code> can be used to delete the Windows Backup Catalog - <code>wbadmin.exe delete catalog -quiet</code>\n* <code>bcdedit.exe</code> can be used to disable automatic Windows recovery features by modifying boot configuration data - <code>bcdedit.exe /set {default} bootstatuspolicy ignoreallfailures & bcdedit /set {default} recoveryenabled no</code>",
        "id":
        "attack-pattern--f5d8eed6-48a9-4cdf-a3d7-d1ffa99c3d2a",
        "x_mitre_platforms": ["Windows", "macOS", "Linux"],
        "object_marking_refs":
        ["marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"],
        "x_mitre_version":
        "1.0",
        "x_mitre_impact_type": ["Availability"],
        "type":
        "attack-pattern",
        "x_mitre_detection":
        "Use process monitoring to monitor the execution and command line parameters of binaries involved in inhibiting system recovery, such as vssadmin, wbadmin, and bcdedit. The Windows event logs, ex. Event ID 524 indicating a system catalog was deleted, may contain entries associated with suspicious activity.\n\nMonitor the status of services involved in system recovery. Monitor the registry for changes associated with system recovery features (ex: the creation of <code>HKEY_CURRENT_USER\\Software\\Policies\\Microsoft\\PreviousVersions\\DisableLocalPage</code>).",
        "created_by_ref":
        "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
        "x_mitre_contributors": ["Yonatan Gotlib, Deep Instinct"],
        "created":
        "2019-04-02T13:54:43.136Z",
        "kill_chain_phases": [{
            "kill_chain_name": "mitre-attack",
            "phase_name": "impact"
        }],
        "external_references": [{
            "source_name":
            "mitre-attack",
            "external_id":
            "T1490",
            "url":
            "https://attack.mitre.org/techniques/T1490"
        }, {
            "description":
            "Mercer, W. and Rascagneres, P. (2018, February 12). Olympic Destroyer Takes Aim At Winter Olympics. Retrieved March 14, 2019.",
            "source_name":
            "Talos Olympic Destroyer 2018",
            "url":
            "https://blog.talosintelligence.com/2018/02/olympic-destroyer.html"
        }, {
            "description":
            "Berry, A., Homan, J., and Eitzman, R. (2017, May 23). WannaCry Malware Profile. Retrieved March 15, 2019.",
            "source_name":
            "FireEye WannaCry 2017",
            "url":
            "https://www.fireeye.com/blog/threat-research/2017/05/wannacry-malware-profile.html"
        }],
        "modified":
        "2019-07-19T14:37:37.347Z"
    }]
}

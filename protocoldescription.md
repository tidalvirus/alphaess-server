# Protocol Description

My attempt at understanding the packets between the Alpha ESS battery and server at www.alphaess.com on port 7777 (in cleartext). Server currently seems to be in Azure, in Singapore. Not noticing any sort of dynamic DNS, or geo IP (tested from hosts in the UK and Australia).

I believe this same system can send commands to discharge the battery to the grid, in times of need as part of *at least* the Shinehub/Powow virtual power plant.

I've currently blocked my home battery system from talking on the Internet, due to this fundamentally flawed setup.

## Packet Fields notes

First 3 fields are single bytes.

### Field 1
Is always '1'

### Field 2
Is either 1, or 2

- 1 - request/push? can be json, or when command 12, is CSV
- 2 - response? ack? Always json style

### Field 3 - Command

Values seen from battery and server: 0, 2, 3, 4, 5, 8, 9, 12, 16

- 0 - Seen before large dump, never has data
- 2 - login request/response?
- 3 - send serial number, get license + home address (WHY) + other info from server
- 4 - battery dumps a bunch of info, similar to command 3 (10 or so packets after command 3).
- 5 - battery dumps more info - just power related though
- 8 - Server requesting last known received data? Battery response with success (what happens in failure?) (what is 'cmdindex'), after this starts a large dump (command 12)
- 9 - Event log dump, next response after success is from server with a request (command 8)
- 12/c - dump from battery in CSV with \n line endings. Each packet with CSV headers is responded to with a success from server
- 16/10 - push from battery to server, json style

All 'sucess' responses seem to match the same code in field 3

### Length

Length seems to be a 4 byte big endian integer - length is of the data (next field). Can be 0, like in command (field 3) 0.

### Data

Data seems to be in ascii, data ends at length exact i.e. code: data = read_bytes(f, length)

### Checksum

Checksum seems to be crc16/modbus, big endian. Found thanks to https://www.scadacore.com/tools/programming-calculators/online-checksum-calculator/

## Login flow

#### Battery:
1, 1, 2

```{"UserName":"[serialnumremoved]","Password":"[removed]","CompanyName":"AlphaESS"}```

#### Server:
1, 2, 2

```{"Status":"Success"}```

#### Battery:
1, 1, 0

[nodata]

#### Server:
1, 2, 0

```{"Status":"Success"}```

#### Battery:
1, 1, 9

```{"MsgType":"EventLog","MsgContent":"21/03/24 10:01:40 41;21/03/24 10:00:46 42;21/03/23 09:10:40 41;21/03/23 09:10:26 42;21/03/21 15:17:27 41;21/03/21 15:07:38 29;21/03/21 15:07:25 30;21/03/21 14:37:28 29;21/03/21 14:37:15 42;21/03/21 14:37:15 30;21/03/21 14:34:20 41;21/03/21 14:34:20 29;21/03/21 14:34:18 27;21/03/21 14:34:18 24;21/03/21 14:34:17 28;21/03/21 14:34:17 23;","Description":"OK"}```

#### Server:
```{"Status":"Success"}```

#### Server:
1, 2, 9

```{"CmdIndex":"82915609","Command":"Resume","Parameter1":"2021/03/24 09:40:13","Parameter2":"21"}```

#### Battery:
1, 2, 8

```{"Command":"Resume","CmdIndex":"82915609","Status":"Success"}```

#### Battery:
1, 1, 12

```Date,Time,SN,Ppv1,Ppv2,Vpv1,Vpv2,Ua,Ub,Uc,Fac,Ubus,PrealL1,PrealL2,PrealL3,Tinv,PacL1,PacL2,PacL3,InvWorkMode,EpvTotal,Einput,Eoutput,Echarge,PmeterL1,PmeterL2,PmeterL3,PmeterDC,Pbat,SOC,BatV,BatC,FlagBms,BmsWork,Pcharge,Pdischarge,BmsRelay,BmsNum,VcellLow,VcellHigh,TcellLow,TcellHigh,IdTempelover,IdTempEover,IdTempediffe,IdChargcurre,IdDischcurre,IdCellvolover,IdCellvollower,IdSoclower,IdCellvoldiffe,BatC1,BatC2,BatC3,BatC4,BatC5,BatC6,SOC1,SOC2,SOC3,SOC4,SOC5,SOC6,ErrInv,WarInv,ErrEms,ErrBms,ErrMeter,ErrBackupBox,EGridCharge,EDischarge,EmsStatus,BmsShutdown,InvBatV,BmuRelay,BmsHardVer1,BmsHardVer2,BmsHardVer3,DispatchSwitch,Pdispatch,DispatchSoc,DispatchMode```
```2021/03/24,09:40:59,[serialnumremoved],1029,981,278.2,288.8,249.3,0.0,0.0,50.02,387,-310,0,0,33,5000,2353,0,3,431.6,60.00,128.40,143.2,0,0,0,951,-2187.8480,26.0,50.18,-43.60,257,1,5050,5050,3,1,17042704,17501462,16908309,16908309,0,0,0,0,0,0,0,0,0,-43.00,0.00,0.00,0.00,0.00,0.00,26.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.10,0,0,0,0,0,0,0,0```
```2021/03/24,09:42:00,[serialnumremoved],1028,998,277.9,285.2,249.8,0.0,0.0,50.03,388,-300,0,0,34,5000,2380,0,3,431.6,60.00,128.40,143.2,-26,0,0,962,-2198.7600,26.4,50.20,-43.80,257,1,5050,5050,3,1,17108241,17501463,16908309,16908309,0,0,0,0,0,0,0,0,0,-43.50,0.00,0.00,0.00,0.00,0.00,26.4,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.20,0,0,0,0,0,0,0,0```
```2021/03/24,09:43:00,[serialnumremoved],1057,1041,278.2,281.6,249.8,0.0,0.0,50.00,389,-280,0,0,34,5000,2392,0,3,431.6,60.00,128.40,143.3,13,0,0,909,-2219.7240,26.8,50.22,-44.20,257,1,5050,5050,3,1,17042707,17501464,16908309,16908309,0,0,0,0,0,0,0,0,0,-44.00,0.00,0.00,0.00,0.00,0.00,26.8,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.20,0,0,0,0,0,0,0,0```

#### Server:
1, 2, 12

```{"Status":"Success"}```

#### Battery:
1, 1, 12

```Date,Time,SN,Ppv1,Ppv2,Vpv1,Vpv2,Ua,Ub,Uc,Fac,Ubus,PrealL1,PrealL2,PrealL3,Tinv,PacL1,PacL2,PacL3,InvWorkMode,EpvTotal,Einput,Eoutput,Echarge,PmeterL1,PmeterL2,PmeterL3,PmeterDC,Pbat,SOC,BatV,BatC,FlagBms,BmsWork,Pcharge,Pdischarge,BmsRelay,BmsNum,VcellLow,VcellHigh,TcellLow,TcellHigh,IdTempelover,IdTempEover,IdTempediffe,IdChargcurre,IdDischcurre,IdCellvolover,IdCellvollower,IdSoclower,IdCellvoldiffe,BatC1,BatC2,BatC3,BatC4,BatC5,BatC6,SOC1,SOC2,SOC3,SOC4,SOC5,SOC6,ErrInv,WarInv,ErrEms,ErrBms,ErrMeter,ErrBackupBox,EGridCharge,EDischarge,EmsStatus,BmsShutdown,InvBatV,BmuRelay,BmsHardVer1,BmsHardVer2,BmsHardVer3,DispatchSwitch,Pdispatch,DispatchSoc,DispatchMode```
```2021/03/24,09:44:01,[serialnumremoved],1057,1041,278.3,281.6,248.5,0.0,0.0,50.02,387,-260,0,0,34,5000,2392,0,3,431.6,60.00,128.40,143.3,0,0,0,902,-2230.6560,27.2,50.24,-44.40,257,1,5050,5050,3,1,16846100,17501465,16908309,16908309,0,0,0,0,0,0,0,0,0,-44.00,0.00,0.00,0.00,0.00,0.00,26.8,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.20,0,0,0,0,0,0,0,0```
```2021/03/24,09:45:01,[serialnumremoved],1043,1039,281.9,281.0,248.5,0.0,0.0,50.00,386,-260,0,0,34,5000,2411,0,3,431.7,60.00,128.40,143.4,0,0,0,898,-2240.7040,27.6,50.24,-44.60,257,1,5050,5050,3,1,17108244,17501465,16908309,16908309,0,0,0,0,0,0,0,0,0,-44.50,0.00,0.00,0.00,0.00,0.00,26.8,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.20,0,0,0,0,0,0,0,0```
```2021/03/24,09:46:02,[serialnumremoved],1027,1039,285.3,281.0,248.8,0.0,0.0,50.03,386,-260,0,0,34,5000,2430,0,3,431.7,60.00,128.40,143.4,-9,0,0,911,-2256.6740,28.0,50.26,-44.90,257,1,5050,5050,3,1,17108245,17501468,16908309,16908309,0,0,0,0,0,0,0,0,0,-44.50,0.00,0.00,0.00,0.00,0.00,28.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.20,0,0,0,0,0,0,0,0```

#### Server:
1, 2, 12

```{"Status":"Success"}```

#### Battery:
1, 1, 12

```Date,Time,SN,Ppv1,Ppv2,Vpv1,Vpv2,Ua,Ub,Uc,Fac,Ubus,PrealL1,PrealL2,PrealL3,Tinv,PacL1,PacL2,PacL3,InvWorkMode,EpvTotal,Einput,Eoutput,Echarge,PmeterL1,PmeterL2,PmeterL3,PmeterDC,Pbat,SOC,BatV,BatC,FlagBms,BmsWork,Pcharge,Pdischarge,BmsRelay,BmsNum,VcellLow,VcellHigh,TcellLow,TcellHigh,IdTempelover,IdTempEover,IdTempediffe,IdChargcurre,IdDischcurre,IdCellvolover,IdCellvollower,IdSoclower,IdCellvoldiffe,BatC1,BatC2,BatC3,BatC4,BatC5,BatC6,SOC1,SOC2,SOC3,SOC4,SOC5,SOC6,ErrInv,WarInv,ErrEms,ErrBms,ErrMeter,ErrBackupBox,EGridCharge,EDischarge,EmsStatus,BmsShutdown,InvBatV,BmuRelay,BmsHardVer1,BmsHardVer2,BmsHardVer3,DispatchSwitch,Pdispatch,DispatchSoc,DispatchMode```
```2021/03/24,09:47:02,[serialnumremoved],1058,1054,286.0,285.1,249.0,0.0,0.0,50.05,387,-300,0,0,34,5000,2467,0,3,432.7,60.00,128.40,143.4,-18,0,0,941,-2292.7680,28.4,50.28,-45.60,257,1,5050,5050,3,1,17042710,17501467,16908309,16908309,0,0,0,0,0,0,0,0,0,-45.00,0.00,0.00,0.00,0.00,0.00,28.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.20,0,0,0,0,0,0,0,0```
```2021/03/24,09:48:03,[serialnumremoved],1083,1079,277.9,276.7,248.8,0.0,0.0,50.02,387,-300,0,0,35,5000,2511,0,3,432.7,60.00,128.40,143.5,-20,0,0,955,-2338.0200,28.8,50.28,-46.50,257,1,5050,5050,3,1,16846104,17501468,16908309,16908309,0,0,0,0,0,0,0,0,0,-46.00,0.00,0.00,0.00,0.00,0.00,28.4,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.30,0,0,0,0,0,0,0,0```
```2021/03/24,09:49:03,[serialnumremoved],1096,1080,274.0,277.0,248.9,0.0,0.0,50.04,385,-300,0,0,35,5000,2551,0,3,432.7,60.00,128.40,143.5,-88,0,0,939,-2359.0700,29.2,50.30,-46.90,257,1,5050,5050,3,1,16846104,17501469,16908309,16908309,0,0,0,0,0,0,0,0,0,-46.50,0.00,0.00,0.00,0.00,0.00,28.4,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.30,0,0,0,0,0,0,0,0```

#### Server:
1, 2, 12

```{"Status":"Success"}```

#### Battery:
1, 1, 12

```Date,Time,SN,Ppv1,Ppv2,Vpv1,Vpv2,Ua,Ub,Uc,Fac,Ubus,PrealL1,PrealL2,PrealL3,Tinv,PacL1,PacL2,PacL3,InvWorkMode,EpvTotal,Einput,Eoutput,Echarge,PmeterL1,PmeterL2,PmeterL3,PmeterDC,Pbat,SOC,BatV,BatC,FlagBms,BmsWork,Pcharge,Pdischarge,BmsRelay,BmsNum,VcellLow,VcellHigh,TcellLow,TcellHigh,IdTempelover,IdTempEover,IdTempediffe,IdChargcurre,IdDischcurre,IdCellvolover,IdCellvollower,IdSoclower,IdCellvoldiffe,BatC1,BatC2,BatC3,BatC4,BatC5,BatC6,SOC1,SOC2,SOC3,SOC4,SOC5,SOC6,ErrInv,WarInv,ErrEms,ErrBms,ErrMeter,ErrBackupBox,EGridCharge,EDischarge,EmsStatus,BmsShutdown,InvBatV,BmuRelay,BmsHardVer1,BmsHardVer2,BmsHardVer3,DispatchSwitch,Pdispatch,DispatchSoc,DispatchMode```
```2021/03/24,09:50:03,[serialnumremoved],1112,1095,278.0,280.8,249.0,0.0,0.0,50.05,388,-370,0,0,35,5000,2615,0,3,432.7,60.00,128.40,143.5,-33,0,0,947,-2435.4880,29.2,50.32,-48.40,257,1,5050,5050,3,1,17108249,17501470,16908309,16908309,0,0,0,0,0,0,0,0,0,-48.00,0.00,0.00,0.00,0.00,0.00,29.2,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.30,0,0,0,0,0,0,0,0```
```2021/03/24,09:51:04,[serialnumremoved],1141,1124,278.3,281.2,248.8,0.0,0.0,50.04,386,-410,0,0,35,5000,2672,0,3,432.8,60.00,128.40,143.6,-22,0,0,968,-2491.8300,29.6,50.34,-49.50,257,1,5050,5050,3,1,17108250,17501473,16908309,16908309,0,0,0,0,0,0,0,0,0,-48.00,0.00,0.00,0.00,0.00,0.00,29.6,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.30,0,0,0,0,0,0,0,0```
```2021/03/24,09:52:04,[serialnumremoved],1107,1095,270.1,281.0,248.8,0.0,0.0,50.04,385,-410,0,0,36,5000,2702,0,3,432.8,60.00,128.40,143.6,-28,0,0,1001,-2517.0000,30.0,50.34,-50.00,257,1,5050,5050,3,1,17108250,17501473,16908309,16908309,0,0,0,0,0,0,0,0,0,-48.00,0.00,0.00,0.00,0.00,0.00,30.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.40,0,0,0,0,0,0,0,0```

#### Server:
1, 2, 12

```{"Status":"Success"}```

#### Battery:
1, 1, 12

```Date,Time,SN,Ppv1,Ppv2,Vpv1,Vpv2,Ua,Ub,Uc,Fac,Ubus,PrealL1,PrealL2,PrealL3,Tinv,PacL1,PacL2,PacL3,InvWorkMode,EpvTotal,Einput,Eoutput,Echarge,PmeterL1,PmeterL2,PmeterL3,PmeterDC,Pbat,SOC,BatV,BatC,FlagBms,BmsWork,Pcharge,Pdischarge,BmsRelay,BmsNum,VcellLow,VcellHigh,TcellLow,TcellHigh,IdTempelover,IdTempEover,IdTempediffe,IdChargcurre,IdDischcurre,IdCellvolover,IdCellvollower,IdSoclower,IdCellvoldiffe,BatC1,BatC2,BatC3,BatC4,BatC5,BatC6,SOC1,SOC2,SOC3,SOC4,SOC5,SOC6,ErrInv,WarInv,ErrEms,ErrBms,ErrMeter,ErrBackupBox,EGridCharge,EDischarge,EmsStatus,BmsShutdown,InvBatV,BmuRelay,BmsHardVer1,BmsHardVer2,BmsHardVer3,DispatchSwitch,Pdispatch,DispatchSoc,DispatchMode```
```2021/03/24,09:53:05,[serialnumremoved],1134,1124,270.2,281.2,248.7,0.0,0.0,50.03,387,-450,0,0,36,5000,2741,0,3,432.8,60.00,128.40,143.7,-4,0,0,986,-2558.2880,30.4,50.36,-50.80,257,1,5050,5050,3,1,17108251,17501473,16908309,16908309,0,0,0,0,0,0,0,0,0,-50.00,0.00,0.00,0.00,0.00,0.00,30.4,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.40,0,0,0,0,0,0,0,0```
```2021/03/24,09:54:05,[serialnumremoved],1137,1119,277.4,273.1,248.9,0.0,0.0,50.03,387,-440,0,0,36,5000,2775,0,3,432.8,60.00,128.40,143.7,-33,0,0,1025,-2573.3960,30.8,50.36,-51.10,257,1,5050,5050,3,1,16846108,17501473,16908309,16908309,0,0,0,0,0,0,0,0,0,-51.00,0.00,0.00,0.00,0.00,0.00,30.8,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.40,0,0,0,0,0,0,0,0```
```2021/03/24,09:55:06,[serialnumremoved],1161,1164,270.2,277.2,248.3,0.0,0.0,50.00,388,-530,0,0,37,5000,2865,0,3,432.8,60.00,128.40,143.8,-79,0,0,1042,-2670.1400,32.0,50.38,-53.00,257,1,5050,5050,3,1,17108252,17501476,16908309,16908309,0,0,0,0,0,0,0,0,0,-51.00,0.00,0.00,0.00,0.00,0.00,32.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.40,0,0,0,0,0,0,0,0```

#### Server:
1, 2, 12

```{"Status":"Success"}```

#### Battery:
1, 1, 12

```Date,Time,SN,Ppv1,Ppv2,Vpv1,Vpv2,Ua,Ub,Uc,Fac,Ubus,PrealL1,PrealL2,PrealL3,Tinv,PacL1,PacL2,PacL3,InvWorkMode,EpvTotal,Einput,Eoutput,Echarge,PmeterL1,PmeterL2,PmeterL3,PmeterDC,Pbat,SOC,BatV,BatC,FlagBms,BmsWork,Pcharge,Pdischarge,BmsRelay,BmsNum,VcellLow,VcellHigh,TcellLow,TcellHigh,IdTempelover,IdTempEover,IdTempediffe,IdChargcurre,IdDischcurre,IdCellvolover,IdCellvollower,IdSoclower,IdCellvoldiffe,BatC1,BatC2,BatC3,BatC4,BatC5,BatC6,SOC1,SOC2,SOC3,SOC4,SOC5,SOC6,ErrInv,WarInv,ErrEms,ErrBms,ErrMeter,ErrBackupBox,EGridCharge,EDischarge,EmsStatus,BmsShutdown,InvBatV,BmuRelay,BmsHardVer1,BmsHardVer2,BmsHardVer3,DispatchSwitch,Pdispatch,DispatchSoc,DispatchMode```
```2021/03/24,09:56:06,[serialnumremoved],1188,1163,270.2,277.1,248.4,0.0,0.0,50.02,388,-580,0,0,37,5000,2939,0,3,432.9,60.00,128.40,143.8,-31,0,0,1051,-2740.6720,32.4,50.38,-54.40,257,1,5050,5050,3,1,17042718,17501477,16908309,17039382,0,0,0,0,0,0,0,0,0,-51.00,0.00,0.00,0.00,0.00,0.00,32.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.50,0,0,0,0,0,0,0,0```
```2021/03/24,09:57:07,[serialnumremoved],1187,1151,269.8,280.9,246.7,0.0,0.0,50.03,384,-100,0,0,37,5000,2088,0,3,432.9,60.00,128.40,143.8,1831,0,0,1040,-2294.5920,32.8,50.32,-45.60,257,1,5050,5050,3,1,17108250,17304862,17170453,16908310,0,0,0,0,0,0,0,0,0,-51.00,0.00,0.00,0.00,0.00,0.00,32.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,51.30,0,0,0,0,0,0,0,0```
```2021/03/24,09:58:07,[serialnumremoved],1206,1158,274.2,269.4,247.9,0.0,0.0,50.03,385,1410,0,0,38,5000,934,0,3,432.9,60.00,128.40,143.9,218,0,0,1069,-815.3260,32.8,50.02,-16.30,257,1,5050,5050,3,1,16911622,16977160,17170453,16908310,0,0,0,0,0,0,0,0,0,-18.50,0.00,0.00,0.00,0.00,0.00,32.8,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,50.70,0,0,0,0,0,0,0,0```

#### Server:
1, 2, 12

```{"Status":"Success"}```

#### Battery:
1, 1, 12

```Date,Time,SN,Ppv1,Ppv2,Vpv1,Vpv2,Ua,Ub,Uc,Fac,Ubus,PrealL1,PrealL2,PrealL3,Tinv,PacL1,PacL2,PacL3,InvWorkMode,EpvTotal,Einput,Eoutput,Echarge,PmeterL1,PmeterL2,PmeterL3,PmeterDC,Pbat,SOC,BatV,BatC,FlagBms,BmsWork,Pcharge,Pdischarge,BmsRelay,BmsNum,VcellLow,VcellHigh,TcellLow,TcellHigh,IdTempelover,IdTempEover,IdTempediffe,IdChargcurre,IdDischcurre,IdCellvolover,IdCellvollower,IdSoclower,IdCellvoldiffe,BatC1,BatC2,BatC3,BatC4,BatC5,BatC6,SOC1,SOC2,SOC3,SOC4,SOC5,SOC6,ErrInv,WarInv,ErrEms,ErrBms,ErrMeter,ErrBackupBox,EGridCharge,EDischarge,EmsStatus,BmsShutdown,InvBatV,BmuRelay,BmsHardVer1,BmsHardVer2,BmsHardVer3,DispatchSwitch,Pdispatch,DispatchSoc,DispatchMode```
```2021/03/24,09:59:08,[serialnumremoved],1187,1173,269.9,272.9,248.1,0.0,0.0,50.03,389,1600,0,0,38,5000,789,0,3,432.9,60.00,128.40,143.9,39,0,0,1071,-674.1900,33.2,49.94,-13.50,257,1,4949,4949,3,1,16846082,17239299,17170453,16908310,0,0,0,0,0,0,0,0,0,-18.50,0.00,0.00,0.00,0.00,0.00,32.8,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,50.60,0,0,0,0,0,0,0,0```
```2021/03/24,10:00:08,[serialnumremoved],1206,1191,274.1,277.1,248.4,0.0,0.0,50.04,390,1630,0,0,38,5000,789,0,3,432.9,60.00,128.40,143.9,4,0,0,1086,-663.9360,33.2,49.92,-13.30,257,1,4949,4949,3,1,16911616,17501443,17170453,16908310,0,0,0,0,0,0,0,0,0,-13.50,0.00,0.00,0.00,0.00,0.00,33.2,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,2.9,138.6,Normal,0,50.60,0,0,0,0,0,0,0,0```

#### Server:
1, 2, 12

```{"Status":"Success"}```

#### Battery:
1, 1, 3

```{"SN":"[serialnumremoved]"}```

#### Server:
1, 2, 3

```{"Status":"Success","SN":"[serialnumremoved]","License":"[removed]","Country":"Australia","Address":"[homeaddressremoved]","ZipCode":"[removed]","PhoneNumber":"123456","Popv":"9.20","Minv":"Storion-GINLANG-S5","Poinv":"4.60","Cobat":"10.10","Mbat":"Smile-BAT-10.1P","Uscapacity":"90.00","ACDC":"3","GridCharge":false,"BatHighCap":"100.00","BatUseCap":"13.00","CtrDis":false,"GridChargeWE":false,"BatHighCapWE":"0.00","BatUseCapWE":"0.00","CtrDisWE":false,"SetMode":"0","SetFeed":"100","SetPhase":"0","CTRate":"120","GeneratorMode":"0","Generator":false,"BackUpBox":false,"Fan":false,"GCSOCStart":"10","GCSOCEnd":"10","GCTimeStart":"0","GCTimeEnd":"0","GCOutputMode":"0","GCChargePower":"0","GCRatedPower":"0","L1Priority":"1","L2Priority":"2","L3Priority":"3","L1SocLimit":"10.00","L2SocLimit":"10.00","L3SocLimit":"10.00","BatReady":"0","Safe":"2","PowerFact":"0","Volt5MinAvg":"0","Volt10MinAvg":"0","TempThreshold":"0","OutCurProtect":"0","DCI":"0","RCD":"0","PvISO":"0","ChargeBoostCur":"0","Channel1":"","ControlMode1":"","StartTime1A":"","EndTime1A":"","StartTime1B":"","EndTime1B":"","ChargeSOC1":"","UPS1":"","SwitchOn1":"0","SwitchOff1":"0","Delay1":"0","Duration1":"0","Pause1":"0","Channel2":"","ControlMode2":"","StartTime2A":"","EndTime2A":"","StartTime2B":"","EndTime2B":"","ChargeSOC2":"","UPS2":"","SwitchOn2":"0","SwitchOff2":"0","Delay2":"0","Duration2":"0","Pause2":"0","ChargeMode1":"0","ChargeMode2":"0","MaxGridCharge":"0.00","InstallMeterOption":"3","InstallModule":"0","StringAE":"0","StringBE":"0","StringCE":"0","PmeterOffset":"0","PmeterMax":"0","DG_Cap":"0","GridMeterCTE":"1","Mmeter":"ACR10R","MeterACNegate":"0","PVMeterCTE":"0","PVMeterCTRate":"0","MeterDCNegate":"0","NetType":"E_Linker","WifiSN":"[removed]","WifiSW":"4720119419R","WifiHW":"AEW2-0002-03","SlaveVersion":"V00.B1","InvHWVersion":"V1.02","SelfUseOrEconomic":"0","ReliefMode":"0","VPPMode":"0","CheckTime":"2021-03-23 11:00:25","TimeChaF1":"0","TimeChaE1":"0","TimeChaF2":"0","TimeChaE2":"0","TimeDisF1":"0","TimeDisE1":"0","TimeDisF2":"0","TimeDisE2":"0","TimeChaFWE1":"0","TimeChaEWE1":"0","TimeChaFWE2":"0","TimeChaEWE2":"0","TimeDisFWE1":"0","TimeDisEWE1":"0","TimeDisFWE2":"0","TimeDisEWE2":"0","OnGridCap":"4250.00","StorageCap":"5000.00","EmsLanguage":0,"Date1":"0","Date2":"0","ChargeWorkDays":"0","ChargeWeekend":"0","SafeSub":"0","POCMeterEnable":"0"}```

#### Battery:
Now seems to start pushing data every 10 seconds

## Data Push

This generally happens every 10 seconds.

#### Battery:

```{"Time":"2021/03/24 10:01:52","SN":"[serialnumremoved]","Ppv1":"1250","Ppv2":"1240","PrealL1":"1630","PrealL2":"0.0","PrealL3":"0.0","PmeterL1":"0","PmeterL2":"0","PmeterL3":"0","PmeterDC":"1065","Pbat":"-688.8960","Sva":"1613","VarAC":"-559","VarDC":"-10","SOC":"33.2"}```

#### Server:
```{"Status":"Success"}```

#### Battery:
```{"Time":"2021/03/24 10:02:02","SN":"[serialnumremoved]","Ppv1":"1245","Ppv2":"1230","PrealL1":"1640","PrealL2":"0.0","PrealL3":"0.0","PmeterL1":"-9","PmeterL2":"0","PmeterL3":"0","PmeterDC":"1077","Pbat":"-688.8960","Sva":"1636","VarAC":"-559","VarDC":"-10","SOC":"33.2"}```

#### Server:
```{"Status":"Success"}```

etc.

## Other dump

Not long after the data push, there is more data, seems similar to the end dump at the initial connection stage

####Battery: 
```{"SN":"[serialnumremoved]","Address":"[homeaddressremoved]","ZipCode":"[removed]","Country":"Australia","PhoneNumber":"123456","License":"[removed]","Popv":"9.2","Minv":"Storion-GINLANG-S5","Poinv":"4.6","Cobat":"10.100","Mbat":"Smile-BAT-10.1P","Uscapacity":"90","InstallMeterOption":"3","Mmeter":"ACR10R","PVMeterMode":"SM60A","BatterySN1":"[removed]","BatterySN2":"0","BatterySN3":"0","BatterySN4":"0","BatterySN5":"0","BatterySN6":"0","BatterySN7":"","BatterySN8":"","BatterySN9":"","BatterySN10":"","BatterySN11":"","BatterySN12":"","BatterySN13":"","BatterySN14":"","BatterySN15":"","BatterySN16":"","BatterySN17":"","BatterySN18":"","BMSVersion":"V1.04","EMSVersion":"V1.01.05","InvVersion":"V00.21", "SlaveVersion":"V00.B1", "InvHWVersion":"V1.02","InvSN":"[removed]","ACDC":"3","Generator":"0","BackUpBox":"False","Fan":"False","GridCharge":"false","CtrDis":"false","TimeChaF1":"0","TimeChaE1":"0","TimeChaF2":"0","TimeChaE2":"0","TimeDisF1":"0","TimeDisE1":"0","TimeDisF2":"0","TimeDisE2":"0","BatHighCap":"100","BatUseCap":"13","SetMode":"0","SetPhase":"0","SetFeed":"100","CTRate":"120","PVMeterCTRate":"0","GridMeterCTE":"1","PVMeterCTE":"0","BakBoxSN":"0","SCBSN":"","BakBoxVer":"0.0.0","SCBVer":"","BMUModel":"","Generator":"0","GeneratorMode":"0","GCSOCStart":"10","GCSOCEnd":"10","GCTimeStart":"0","GCTimeEnd":"0","GCOutputMode":"0","GCChargePower":"0","GCRatedPower":"0","EmsLanguage":"0","L1Priority":"1","L2Priority":"2","L3Priority":"3","L1SocLimit":"10","L2SocLimit":"10","L3SocLimit":"10","FirmwareVersion":"V1.01","OnGridCap":"4250","StorageCap":"5000","BatReady":"0","MeterACNegate":"0","MeterDCNegate":"0","Safe":"2","PowerFact":"0","Volt5MinAvg":"0","Volt10MinAvg":"0","TempThreshold":"0","OutCurProtect":"0","DCI":"0","RCD":"0","PvISO":"0","ChargeBoostCur":"0","Channel1":"0","ControlMode1":"0","StartTime1A":"0","EndTime1A":"0","StartTime1B":"0","EndTime1B":"0","Date1":"0","ChargeSOC1":"0","ChargeMode1":"0","UPS1":"0","SwitchOn1":"0","SwitchOff1":"0","Delay1":"0","Duration1":"0","Pause1":"0","Channel2":"0","ControlMode2":"0","StartTime2A":"0","EndTime2A":"0","StartTime2B":"0","EndTime2B":"0","Date2":"0","ChargeSOC2":"0","ChargeMode2":"0","UPS2":"0","SwitchOn2":"0","SwitchOff2":"0","Delay2":"0","Duration2":"0","Pause2":"0","NetType":"E_Linker","WifiSN":"[removed]","WifiSW":"4720119419R","WifiHW":"AEW2-0002-03"}```

#### Server:
No obvious response

Goes back to one data push after this, the sends the below.

#### Battery:
```{"SN":""[serialnumremoved]","Address":"[homeaddressremoved]","ZipCode":"[removed]","Country":"Australia","PhoneNumber":"123456","License":"[removed]","Popv":"9.2","Minv":"Storion-GINLANG-S5","Poinv":"4.6","Cobat":"10.100","Mbat":"Smile-BAT-10.1P","Uscapacity":"90","InstallMeterOption":"3","Mmeter":"ACR10R","PVMeterMode":"SM60A","BatterySN1":"2012050546","BatterySN2":"0","BatterySN3":"0","BatterySN4":"0","BatterySN5":"0","BatterySN6":"0","BatterySN7":"","BatterySN8":"","BatterySN9":"","BatterySN10":"","BatterySN11":"","BatterySN12":"","BatterySN13":"","BatterySN14":"","BatterySN15":"","BatterySN16":"","BatterySN17":"","BatterySN18":"","BMSVersion":"V1.04","EMSVersion":"V1.01.05","InvVersion":"V00.21", "SlaveVersion":"V00.B1", "InvHWVersion":"V1.02","InvSN":"134F3220C050285","ACDC":"3","Generator":"0","BackUpBox":"False","Fan":"False","GridCharge":"false","CtrDis":"false","TimeChaF1":"0","TimeChaE1":"0","TimeChaF2":"0","TimeChaE2":"0","TimeDisF1":"0","TimeDisE1":"0","TimeDisF2":"0","TimeDisE2":"0","BatHighCap":"100","BatUseCap":"13","SetMode":"0","SetPhase":"0","SetFeed":"100","CTRate":"120","PVMeterCTRate":"0","GridMeterCTE":"1","PVMeterCTE":"0","BakBoxSN":"0","SCBSN":"","BakBoxVer":"0.0.0","SCBVer":"","BMUModel":"","Generator":"0","GeneratorMode":"0","GCSOCStart":"10","GCSOCEnd":"10","GCTimeStart":"0","GCTimeEnd":"0","GCOutputMode":"0","GCChargePower":"0","GCRatedPower":"0","EmsLanguage":"0","L1Priority":"1","L2Priority":"2","L3Priority":"3","L1SocLimit":"10","L2SocLimit":"10","L3SocLimit":"10","FirmwareVersion":"V1.01","OnGridCap":"4250","StorageCap":"5000","BatReady":"0","MeterACNegate":"0","MeterDCNegate":"0","Safe":"2","PowerFact":"0","Volt5MinAvg":"0","Volt10MinAvg":"0","TempThreshold":"0","OutCurProtect":"0","DCI":"0","RCD":"0","PvISO":"0","ChargeBoostCur":"0","Channel1":"0","ControlMode1":"0","StartTime1A":"0","EndTime1A":"0","StartTime1B":"0","EndTime1B":"0","Date1":"0","ChargeSOC1":"0","ChargeMode1":"0","UPS1":"0","SwitchOn1":"0","SwitchOff1":"0","Delay1":"0","Duration1":"0","Pause1":"0","Channel2":"0","ControlMode2":"0","StartTime2A":"0","EndTime2A":"0","StartTime2B":"0","EndTime2B":"0","Date2":"0","ChargeSOC2":"0","ChargeMode2":"0","UPS2":"0","SwitchOn2":"0","SwitchOff2":"0","Delay2":"0","Duration2":"0","Pause2":"0","NetType":"E_Linker","WifiSN":"E470120B0575","WifiSW":"4720119419R","WifiHW":"AEW2-0002-03"}```

#### Server:
```{"Status":"Success"}```

And back to regular data push after this, one time, then 'data dump 2'

## Data Dump 2

#### Battery:
```{"Time":"2021/03/24 10:02:40","SN":"[serialnumremoved]","Ppv1":"1243","Ppv2":"1228","Upv1":"270.3","Upv2":"273.0","Ua":"248.2","Ub":"0.0","Uc":"0.0","Fac":"50.00","Ubus":"383","PrealL1":"1640","PrealL2":"0.0","PrealL3":"0.0","Tinv":"38","PacL1":"5000","PacL2":"822","PacL3":"0.0","InvWorkMode":"3","EpvTotal":"433.0","Einput":"60.00","Eoutput":"128.40","Echarge":"143.9","PmeterL1":"-4","PmeterL2":"0","PmeterL3":"0","PmeterDC":"1071","Pbat":"-708.8640","SOC":"33.6","BatV":"49.92","BatC":"-14.20","FlagBms":"257","BmsWork":"1","Pcharge":"4949","Pdischarge":"4949","BmsRelay":"3","BmsNum":"1","VcellLow":"17173759","VcellHigh":"17501442","TcellLow":"17170453","TcellHigh":"16908310","IdTempelover":"0","IdTempEover":"0","IdTempediffe":"0","IdChargcurre":"0","IdDischcurre":"0","IdCellvolover":"0","IdCellvollower":"0","IdSoclower":"0","IdCellvoldiffe":"0","BatC1":"-14.00","BatC2":"0.00","BatC3":"0.00","BatC4":"0.00","BatC5":"0.00","BatC6":"0.00","SOC1":"33.6","SOC2":"0.0","SOC3":"0.0","SOC4":"0.0","SOC5":"0.0","SOC6":"0.0","ErrInv":"0","WarInv":"0","ErrEms":"0","ErrBms":"0","ErrMeter":"0","ErrBackupBox":"0","EGridCharge":"2.9","EDischarge":"138.6","EmsStatus":"Normal","InvBatV":"50.60","BmsShutdown":"0","BmuRelay":"0","BmsHardVer1":"0", "BmsHardVer2":"0", "BmsHardVer3":"0","DispatchSwitch":"0","Pdispatch":"0", "DispatchSoc":"0", "DispatchMode":"0","PMeterDCL1":"1071","PMeterDCL2":"0", "PMeterDCL3":"0","MeterDCUa":"248.3","MeterDCUb":"0.0", "MeterDCUc":"0.0","Eirp":"-63","CSQ":"99,99"}```

#### Server:
```{"Status":"Success"}```

And back to regular data push after this.

# Other notes

## Streaming Oddities/Bugs

The battery streams data every 10 seconds (1, 1, 16 header). In that stream is a timestamp of, I guess, the time the data was gathered. A point in time capture is my assumption.

### Oddity 1

Sometimes the battery will send the same timestamped data twice, with a normal spacing of 10 seconds. This is the exact same data it just sent 10 seconds ago. At the same time, it also sends the expected timestamp (data from 10 seconds later).

### Oddity 2

Sometimes the battery won't stream every 10 seconds, and will collect up two or more 10 second streams and send them at the same time.

Neither of these would be a real problem if I could set the time on the battery. It is not set by NTP, so I can only presume it's set by the server. After just a few weeks in operation without communication with the real www.alphaess.com system, it is now still in DST, and has also drifted by 1m20s.

## Insecurity of Reconnection Without Re-Authentication

The battery seems to take a broken TCP connection to the server as just something to reconnect, and start sending data again. Does not provide login details, just starts streaming the data every 10 seconds as if nothing happened.
Sure, the system is insecure in the first place, but this makes it even easier for a man in the middle attack, as the server doesn't block data being sent, nor does the battery seem to care that something happened to the TCP connection.

I'm not sure how long the battery waits before it wants to authenticate again.
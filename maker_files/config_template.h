/*
 * config.h
 *
 * Created: 26-12-2013 12:18:30
 *	Author: Prateek
 */ 

#ifndef CONFIG_H_
#define CONFIG_H_

#include <irq.h>

// #define DEBUG_MODE							//	Enable Debug msgs.
#define CS_INDIRECT_POLL_RATE		250		//	in ms. Polling rate for ack or other packets.
#define NWK_JOIN_FAIL_THRESHOLD		0x01	//	force system to sleep if device not join nwk.

//	channel to join.
#define CHANNEL_MASK		(1l << 0x1a)

// pan nwk to join.
#define EXT_PANID			0xAAAAAAAAAAAAAAAALL

// device selection.
#define LUX_DEVICE				// to use Lux Sensor.
#define HT_DEVICE				// to use HT Sensor.

// device addressing.
#define DEVICE_ID_MASK			0xFFFF000000000000LL
#define DEVICE_ID				0x5003000000000000LL
#define SENSOR_ID				0x1037LL

// sensor info
#define LUX_SENSOR_ID			0x4A		//	Lux Sensor SlaveID.
#define HT_SENSOR_ID			0x40		//	HT Sensor SlaveID.

// lowest threshold value for Lux
#define LUX_LOWEST_THERSHOLD	0x2F		//	0x2F means luxVal= 45.9

// sampling time period to be chages as per rate of change of temperature and rate of change of temperature.
#define LOW_LVL_CHANGE		.1		// when change is lower than 0.1*C.
#define HIG_LVL_CHANGE		.2		// when change is Higher than 0.2*C.
#define LOW_SAMPLING_SLEEP_TIME		3		//	Time for sleep in mins when change of rate of temp is low.
#define MOD_SAMPLING_SLEEP_TIME		2		//	Time for sleep in mins when change of rate of temp is moderate.
#define HIGH_SAMPLING_SLEEP_TIME	1		//	Time for sleep in mins when change of rate of temp is high.

// absolute max time interval between 2 data packets.
#define MAX_WAIT_TIME			30	//	max wait time to change temperature over deltaTime.
#define NON_NWK_SLEEP			30	//	time to sleep with no interrupt in case no nwk.

// sensor interrupt for lux sensor.
#define SENSOR_INTR_PIN		18
#define SENSOR_INTR			IRQ_EIC_EXTINT2

// defferent temperature ranges and there respective change value to send packet.
// Ranges should be in ascending order.
#define TEMP_RANGE_01			1
#define TEMP_RANGE_01_LOW		0
#define TEMP_RANGE_01_HIGH		18.2
#define TEMP_RANGE_01_DEL		1.0		// DeltaT needed before sending data while in range 1.

#define TEMP_RANGE_02			2
#define TEMP_RANGE_02_LOW		17.8
#define TEMP_RANGE_02_HIGH		20.2
#define TEMP_RANGE_02_DEL		0.5		// DeltaT needed before sending data while in range 2.

#define TEMP_RANGE_03			3
#define TEMP_RANGE_03_LOW		19.8
#define TEMP_RANGE_03_HIGH		21.2
#define TEMP_RANGE_03_DEL		0.4		// DeltaT needed before sending data while in range 3.

#define TEMP_RANGE_04			4
#define TEMP_RANGE_04_LOW		20.8
#define TEMP_RANGE_04_HIGH		22.2
#define TEMP_RANGE_04_DEL		0.3		// DeltaT needed before sending data while in range 4.

#define TEMP_RANGE_05			5
#define TEMP_RANGE_05_LOW		21.8
#define TEMP_RANGE_05_HIGH		23.2
#define TEMP_RANGE_05_DEL		0.2		// DeltaT needed before sending data while in range 5.

#define TEMP_RANGE_06			6
#define TEMP_RANGE_06_LOW		22.8
#define TEMP_RANGE_06_HIGH		24.2
#define TEMP_RANGE_06_DEL		0.2		// DeltaT needed before sending data while in range 6.

#define TEMP_RANGE_07			7
#define TEMP_RANGE_07_LOW		23.8
#define TEMP_RANGE_07_HIGH		25.2
#define TEMP_RANGE_07_DEL		0.3		// DeltaT needed before sending data while in range 7.

#define TEMP_RANGE_08			8
#define TEMP_RANGE_08_LOW		24.8
#define TEMP_RANGE_08_HIGH		26.2
#define TEMP_RANGE_08_DEL		0.4		// DeltaT needed before sending data while in range 8.

#define TEMP_RANGE_09			9
#define TEMP_RANGE_09_LOW		25.8
#define TEMP_RANGE_09_HIGH		28.2
#define TEMP_RANGE_09_DEL		0.5		// DeltaT needed before sending data while in range 9.

#define TEMP_RANGE_10			10
#define TEMP_RANGE_10_LOW		27.8
#define TEMP_RANGE_10_HIGH		40.2
#define TEMP_RANGE_10_DEL		1.0		// DeltaT needed before sending data while in range 10.

#define NUM_OF_PACKET_TO_CHECK_BATMON		2000		//	Num of packets before rechecking Batmon Reg.


#endif /* CONFIG_H_ */


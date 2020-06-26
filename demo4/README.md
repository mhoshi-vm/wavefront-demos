## Getting Started

This demo, intentionally removes slueth and wavefront plugin and instead use the java agent <br>
<br>
https://www.wavefront.com/wavefront-tracing-agent-for-java/ <br>
<br>

First remove all dependices from pom.xml<br>

```
<!-- 		<dependency>
			<groupId>com.wavefront</groupId>
			<artifactId>wavefront-spring-boot-starter</artifactId>
		</dependency>
		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-starter-sleuth</artifactId>
		</dependency> -->
```

Then build jar 

```
mvn clean package
```
Run the static attachment

```
java -javaagent:opentracing-specialagent-1.7.3.jar -Dsa.tracer=wavefront  -Dwf.token=`cat ~/.wavefront_freemium` -jar target/demo-0.0.1-SNAPSHOT.jar
```

Should show below

```
Deprecated key (as of v1.7.0): "sa.tracer" should be changed to "sa.exporter"
Jun 26, 2020 4:31:02 PM com.wavefront.opentracing.Configuration loadConfigurationFile
INFO: Successfully loaded Tracer configuration file tracer.properties
Jun 26, 2020 4:31:02 PM com.wavefront.opentracing.TracerParameters getParameters
INFO: Retrieved Tracer parameter wf.reportingMechanism=direct
Jun 26, 2020 4:31:02 PM com.wavefront.opentracing.TracerParameters getParameters
INFO: Retrieved Tracer parameter wf.customTagsDelimiter=,
Jun 26, 2020 4:31:02 PM com.wavefront.opentracing.TracerParameters getParameters
INFO: Retrieved Tracer parameter wf.service=hello-wo-slueth
Jun 26, 2020 4:31:02 PM com.wavefront.opentracing.TracerParameters getParameters
INFO: Retrieved Tracer parameter wf.token=XXXXXXXXXXXXXXXXXX
Jun 26, 2020 4:31:02 PM com.wavefront.opentracing.TracerParameters getParameters
INFO: Retrieved Tracer parameter wf.server=https://wavefront.surf
Jun 26, 2020 4:31:02 PM com.wavefront.opentracing.TracerParameters getParameters
INFO: Retrieved Tracer parameter wf.application=demo4
.==============================================================.
|                    Static Deferred Attach                    |
|                    Enabled: true (default)                   |
|==============================================================|
|               To disable Static Deferred Attach,             |
|                 specify -Dsa.init.defer=false                |
|=============================================================='
' 1 deferrers were detected:
```

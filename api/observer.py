from opentelemetry import metrics
from opentelemetry.sdk.resources import (
    Resource, 
    SERVICE_NAME,
    SERVICE_VERSION
)
from opentelemetry.sdk.metrics import (
    MeterProvider
)
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader
)
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter
)

reader_otlp = PeriodicExportingMetricReader(
    OTLPMetricExporter()
)

resource = Resource(
    attributes={
        SERVICE_NAME: 'budget-api',
        SERVICE_VERSION: '1.0.0'
    }
)

provider = MeterProvider(
    resource=resource,
    metric_readers=[reader_otlp]
)

metrics.set_meter_provider(provider)
meter = metrics.get_meter('meter')

request_counter = meter.create_counter(
    name='request_counter',
    unit='1',
    description='Total de requests'
)



import pulumi
from isodate import Duration, duration_isoformat
from pulumi_azure import core, storage, servicebus


# Create an Azure Resource Group
resource_group = core.ResourceGroup(
    'messaging-samples',
    location='EastUs',
    name='messaging-samples')

# Create an Azure Service Bus namespace
sbnamespace = servicebus.Namespace('ns-messaging-samples',
                                   sku='Standard',
                                   name='ns-messaging-samples',
                                   location='EastUs',
                                   resource_group_name=resource_group.name
                                   )

# Create an associated queue within the above namespace
servicebus.Queue('simplequeue',
                 name='simplequeue',
                 namespace_name=sbnamespace.name,
                 dead_lettering_on_message_expiration=True,
                 resource_group_name=resource_group.name,
                 max_size_in_megabytes=1024,
                 default_message_ttl=duration_isoformat(Duration(days=5))
                 )


# Export the connection string for the storage account
pulumi.export('namespace_id', sbnamespace.id)
pulumi.export('namespace_name', sbnamespace.name)

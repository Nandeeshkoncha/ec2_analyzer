import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:project','Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

@click.group()
def instances():
    "List of commands"
@instances.command('list')
@click.option('--project',default=None,
    help="only instance for project(tag Project:<name>)")
def list_instances(project):
    "list of instances"
    instances = filter_instances(project)

    for i in instances:
        tags = {t['Key'] : t['Value'] for t in i.tags or []}
        print(','.join((i.instance_id,i.instance_type,i.placement['AvailabilityZone'],
        i.state['Name'],i.public_dns_name,tags.get('project','<no project>')
        )))

    return

@instances.command('stop')
@click.option('--project',default=None,
    help="Only instances for Project")
def stop_instances(project):
    "stop EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("stopping {0}....".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project',default=None,
    help="Only instances for Project")
def stop_instances(project):
    "start EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("starting {0}....".format(i.id))
        i.start()

    return


if __name__ == '__main__':
    instances()

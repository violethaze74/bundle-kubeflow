"""Runs tests by inspecting microk8s with kubectl."""

from time import sleep

import pytest
import yaml
from flaky import flaky
from sh import Command

try:
    from sh import juju_kubectl as kubectl
except ImportError:
    kubectl = Command('kubectl').bake('-nkubeflow')


def get_statuses():
    """Gets names and statuses of all workload pods.

    Uses Juju 2.8 label first, and if that's empty, tries Juju 2.9 label
    """

    pods = yaml.safe_load(kubectl.get('pods', '-ljuju-app', '-oyaml').stdout)

    if pods['items']:
        return {i['metadata']['labels']['juju-app']: i['status']['phase'] for i in pods['items']}
    else:
        pods = yaml.safe_load(kubectl.get('pods', '-lapp.kubernetes.io/name', '-oyaml').stdout)
        return {
            i['metadata']['labels']['app.kubernetes.io/name']: i['status']['phase']
            for i in pods['items']
        }


@pytest.mark.full
@flaky(max_runs=60, rerun_filter=lambda *_: sleep(5) or True)
def test_running_full():
    assert get_statuses() == {
        'admission-webhook': 'Running',
        'argo-controller': 'Running',
        'argo-server': 'Running',
        'dex-auth': 'Running',
        'envoy': 'Running',
        'istio-ingressgateway': 'Running',
        'istio-pilot': 'Running',
        'jupyter-controller': 'Running',
        'jupyter-ui': 'Running',
        'katib-controller': 'Running',
        'katib-db': 'Running',
        'katib-db-manager': 'Running',
        'katib-ui': 'Running',
        'kfp-api': 'Running',
        'kfp-db': 'Running',
        'kfp-persistence': 'Running',
        'kfp-profile-controller': 'Running',
        'kfp-schedwf': 'Running',
        'kfp-ui': 'Running',
        'kfp-viewer': 'Running',
        'kfp-viz': 'Running',
        'kubeflow-dashboard': 'Running',
        'kubeflow-profiles': 'Running',
        'kubeflow-volumes': 'Running',
        'kubeflow-roles': 'Running',
        'kubeflow-metacontroller-operator-charm': 'Running',
        'metacontroller-operator': 'Running',
        'minio': 'Running',
        'mlmd': 'Running',
        'oidc-gatekeeper': 'Running',
        'seldon-controller-manager': 'Running',
        'tensorboard-controller': 'Running',
        'tensorboards-web-app': 'Running',
        'training-operator': 'Running',
    }


@pytest.mark.lite
@flaky(max_runs=60, rerun_filter=lambda *_: sleep(5) or True)
def test_running_lite():
    assert get_statuses() == {
        'admission-webhook': 'Running',
        'argo-controller': 'Running',
        'dex-auth': 'Running',
        'istio-ingressgateway': 'Running',
        'istio-pilot': 'Running',
        'jupyter-controller': 'Running',
        'jupyter-ui': 'Running',
        'kfp-api': 'Running',
        'kfp-db': 'Running',
        'kfp-persistence': 'Running',
        'kfp-schedwf': 'Running',
        'kfp-ui': 'Running',
        'kfp-viewer': 'Running',
        'kfp-viz': 'Running',
        'kubeflow-dashboard': 'Running',
        'kubeflow-profiles': 'Running',
        'kubeflow-roles': 'Running',
        'kubeflow-volumes': 'Running',
        'metacontroller-operator': 'Running',
        'minio': 'Running',
        'mlmd': 'Running',
        'oidc-gatekeeper': 'Running',
        'seldon-controller-manager': 'Running',
        'training-operator': 'Running',
    }


@pytest.mark.full
def test_crd_created_full():
    crds = yaml.safe_load(kubectl.get('crd', '-oyaml').stdout)

    names = {i['metadata']['name'] for i in crds['items']}
    assert names.issuperset(
        {
            'experiments.kubeflow.org',
            'notebooks.kubeflow.org',
            'poddefaults.kubeflow.org',
            'profiles.kubeflow.org',
            'scheduledworkflows.kubeflow.org',
            'seldondeployments.machinelearning.seldon.io',
            'servicerolebindings.rbac.istio.io',
            'serviceroles.rbac.istio.io',
            'suggestions.kubeflow.org',
            'trials.kubeflow.org',
            'viewers.kubeflow.org',
            'workflows.argoproj.io',
            'xgboostjobs.kubeflow.org',
            'mxjobs.kubeflow.org',
            'pytorchjobs.kubeflow.org',
            'tfjobs.kubeflow.org',
        }
    )


@pytest.mark.lite
def test_crd_created_lite():
    crds = yaml.safe_load(kubectl.get('crd', '-oyaml').stdout)

    names = {i['metadata']['name'] for i in crds['items']}
    assert names.issuperset(
        {
            'notebooks.kubeflow.org',
            'poddefaults.kubeflow.org',
            'profiles.kubeflow.org',
            'scheduledworkflows.kubeflow.org',
            'seldondeployments.machinelearning.seldon.io',
            'servicerolebindings.rbac.istio.io',
            'serviceroles.rbac.istio.io',
            'viewers.kubeflow.org',
            'workflows.argoproj.io',
            'xgboostjobs.kubeflow.org',
            'mxjobs.kubeflow.org',
            'pytorchjobs.kubeflow.org',
            'tfjobs.kubeflow.org',
        }
    )


@pytest.mark.full
def test_service_accounts_created_full():
    sas = yaml.safe_load(kubectl.get('sa', '-oyaml').stdout)
    names = {i['metadata']['name'] for i in sas['items']}
    assert names.issuperset(
        {
            'admission-webhook',
            'admission-webhook-operator',
            'argo-controller',
            'argo-controller-operator',
            'argo-server',
            'argo-server-operator',
            'default',
            'dex-auth',
            'dex-auth-operator',
            'envoy-operator',
            'istio-ingressgateway-operator',
            'istio-ingressgateway-operator-operator',
            'istio-pilot',
            'istio-pilot-operator',
            'jupyter-controller',
            'jupyter-controller-operator',
            'jupyter-ui',
            'jupyter-ui-operator',
            'katib-controller',
            'katib-controller-operator',
            'katib-db-manager',
            'katib-db-manager-operator',
            'katib-db-operator',
            'katib-ui',
            'katib-ui-operator',
            'kfp-api',
            'kfp-api-operator',
            'kfp-db-operator',
            'kfp-persistence',
            'kfp-persistence-operator',
            'kfp-profile-controller-operator',
            'kfp-schedwf',
            'kfp-schedwf-operator',
            'kfp-ui',
            'kfp-ui-operator',
            'kfp-viewer',
            'kfp-viewer-operator',
            'kfp-viz-operator',
            'kubeflow-dashboard',
            'kubeflow-dashboard-operator',
            'kubeflow-profiles',
            'kubeflow-profiles-operator',
            'kubeflow-roles',
            'kubeflow-volumes',
            'kubeflow-volumes-operator',
            'metacontroller-operator',
            'metacontroller-operator-charm',
            'minio-operator',
            'mlmd-operator',
            'modeloperator',
            'oidc-gatekeeper-operator',
            'seldon-controller-manager',
            'seldon-controller-manager-operator',
            'spark',
            'spark-operator',
            'tensorboard-controller',
            'tensorboard-controller-operator',
            'tensorboards-web-app',
            'tensorboards-web-app-operator',
            'training-operator',
        },
    )


@pytest.mark.lite
def test_service_accounts_created_lite():
    sas = yaml.safe_load(kubectl.get('sa', '-oyaml').stdout)

    names = {i['metadata']['name'] for i in sas['items']}
    assert names.issuperset(
        {
            'admission-webhook',
            'admission-webhook-operator',
            'argo-controller',
            'argo-controller-operator',
            'default',
            'dex-auth',
            'dex-auth-operator',
            'istio-ingressgateway',
            'istio-ingressgateway-operator',
            'istio-pilot',
            'istio-pilot-operator',
            'jupyter-controller',
            'jupyter-controller-operator',
            'jupyter-ui',
            'jupyter-ui-operator',
            'kfp-api',
            'kfp-api-operator',
            'kfp-db-operator',
            'kfp-persistence',
            'kfp-persistence-operator',
            'kfp-schedwf',
            'kfp-schedwf-operator',
            'kfp-ui',
            'kfp-ui-operator',
            'kfp-viewer',
            'kfp-viewer-operator',
            'kfp-viz-operator',
            'kubeflow-dashboard',
            'kubeflow-dashboard-operator',
            'kubeflow-profiles',
            'kubeflow-profiles-operator',
            'kubeflow-volumes',
            'kubeflow-volumes-operator',
            'minio-operator',
            'mlmd-operator',
            'oidc-gatekeeper-operator',
            'pipeline-runner',
            'seldon-controller-manager',
            'seldon-controller-manager-operator',
            'training-operator',
        },
    )


@pytest.mark.edge
def test_service_accounts_created_edge():
    sas = yaml.safe_load(kubectl.get('sa', '-oyaml').stdout)

    names = {i['metadata']['name'] for i in sas['items']}
    assert names.issuperset(
        {
            'argo-controller',
            'argo-controller-operator',
            'default',
            'kfp-api',
            'kfp-api-operator',
            'kfp-db-operator',
            'kfp-persistence',
            'kfp-persistence-operator',
            'kfp-schedwf',
            'kfp-schedwf-operator',
            'minio-operator',
            'pipeline-runner',
            'seldon-controller-manager',
            'seldon-controller-manager-operator',
            'training-operator',
        },
    )

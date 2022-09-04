"""Data loading module for user-side."""
import os
from typing import List, Union

from dgl import DGLGraph

import gli.dataset
from gli import ROOT_PATH
from gli.graph import read_gli_graph
from gli.task import GLITask, read_gli_task
from gli.utils import download_data


def combine_graph_and_task(graph: Union[DGLGraph, List[DGLGraph]],
                           task: GLITask):
    """Combine graph and task to get a GLI dataset.

    Args:
        graph (Union[DGLGraph, List[DGLGraph]]): Graph(s) to construct dataset.
        task (GLITask): GLI task config

    Raises:
        NotImplementedError: Unknown task type

    Returns:
        DGLDataset
    """
    if task.type in ("NodeClassification", "NodeRegression"):
        return gli.dataset.node_dataset_factory(graph, task)
    elif task.type in ("GraphClassification", "GraphRegression"):
        return gli.dataset.graph_dataset_factory(graph, task)
    elif task.type in ("TimeDependentLinkPrediction", "LinkPrediction",
                       "KGEntityPrediction", "KGRelationPrediction"):
        return gli.dataset.edge_dataset_factory(graph, task)
    raise NotImplementedError(f"Unsupported type {task.type}")


def get_gli_dataset(dataset: str, task: str, device="cpu", verbose=True):
    """Get a known GLI dataset of a given task.

    Args:
        dataset (str): Name of dataset.
        task (str): Name of task file.
        device (str, optional): Returned dataset's device. Defaults to "cpu".
        verbose (bool, optional): Defaults to True.

    Returns:
        Dataset: a iterable dataset of a given task.
    """
    g = get_gli_graph(dataset, device=device, verbose=verbose)
    t = get_gli_task(dataset, task, verbose=verbose)
    return combine_graph_and_task(g, t)


def get_gli_graph(dataset: str, device="cpu", verbose=True):
    """Get a known GLI graph.

    Download dependent files if needed.

    Args:
        dataset (str): Name of dataset.
        device (str, optional): Returned graph's device. Defaults to "cpu".
        verbose (bool, optional): Defaults to True.

    Returns:
        DGLHeteroGraph: Graph object(s) that represents the dataset.
    """
    data_dir = os.path.join(ROOT_PATH, "datasets/", dataset)
    metadata_path = os.path.join(data_dir, "metadata.json")
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"{data_dir} not found.")
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"{metadata_path} not found.")
    download_data(dataset, verbose=verbose)

    return read_gli_graph(metadata_path, device=device, verbose=verbose)


def get_gli_task(dataset: str, task: str, verbose=True):
    """Get a known GLI task of a given dataset.

    Args:
        dataset (str): Name of dataset.
        task (str): Name of task.
        verbose (bool, optional): Defaults to True.

    Returns:
        GLITask: Predefined GLI task.
    """
    data_dir = os.path.join(ROOT_PATH, "datasets/", dataset)
    task_path = os.path.join(data_dir, f"{task}.json")
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"{data_dir} not found.")
    if not os.path.exists(task_path):
        raise FileNotFoundError(f"{task_path} not found.")
    download_data(dataset, verbose=verbose)

    return read_gli_task(task_path, verbose=verbose)
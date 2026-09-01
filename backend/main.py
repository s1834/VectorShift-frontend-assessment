from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from collections import defaultdict, deque

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pipeline(BaseModel):
    nodes: list
    edges: list


@app.post("/pipelines/parse")

def parse_pipeline(pipeline: Pipeline):

    graph = defaultdict(list)
    indegree = defaultdict(int)

    for node in pipeline.nodes:
        indegree[node["id"]] = 0

    for edge in pipeline.edges:
        graph[edge["source"]].append(edge["target"])
        indegree[edge["target"]] += 1

    q = deque()

    for node in indegree:
        if indegree[node] == 0:
            q.append(node)

    visited = 0

    while q:
        node = q.popleft()
        visited += 1

        for nxt in graph[node]:
            indegree[nxt] -= 1

            if indegree[nxt] == 0:
                q.append(nxt)

    return {
        "num_nodes": len(pipeline.nodes),
        "num_edges": len(pipeline.edges),
        "is_dag": visited == len(pipeline.nodes),
    }
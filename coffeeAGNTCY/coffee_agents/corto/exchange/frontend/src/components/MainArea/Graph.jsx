import React, { useEffect } from 'react';
import {
    ReactFlow,
    ReactFlowProvider,
    useNodesState,
    useEdgesState,
    Controls,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import CustomEdge from './Edge';

const DELAY_DURATION = 1000; // Duration for each animation step in milliseconds
const proOptions = { hideAttribution: true };

// Constants for node and edge IDs
const NODE_IDS = {
    BUYER: '1',
    SOMMELIER: '2',
};

const EDGE_IDS = {
    BUYER_TO_SOMMELIER: '1-2',
};

// Initial nodes and edges
const initialNodes = [
    {
        id: NODE_IDS.BUYER,
        type: 'input',
        data: { label: 'Buyer' },
        position: { x: 250, y: 50 },
        style: {
            fontFamily: "'CiscoSansTT'",
            border: '1px solid #187ADC',
            backgroundColor: 'rgba(24, 122, 220, 0.3)',
            color: '#000000',
            fontWeight: '100',
            padding: 10,
            borderRadius: 5,
        },
    },
    {
        id: NODE_IDS.SOMMELIER,
        type: 'output',
        data: {
            label: (
                <div>
                    Sommelier
                    <div style={{ fontSize: '.65em' }}>
                        (Q Grader)
                    </div>
                </div>
            ),
        },
        position: { x: 250, y: 250 },
        style: {
            fontFamily: "'CiscoSansTT'",
            border: '1px solid #187ADC',
            backgroundColor: 'rgba(24, 122, 220, 0.3)',
            color: '#000000',
            fontWeight: '100',
            padding: 10,
            borderRadius: 5,
        },
    },
];

const initialEdges = [
    {
        id: EDGE_IDS.BUYER_TO_SOMMELIER,
        source: NODE_IDS.BUYER,
        target: NODE_IDS.SOMMELIER,
        style: { stroke: '#187ADC', strokeWidth: 2 },
        data: {
            label: 'A2A : SLIM',
            edgeColor: '#187ADC',
            labelColor: '#FFFFFF',
            labelBackgroundColor: '#187ADC',
        },
        type: 'custom',
    },
];

const edgeTypes = {
    custom: CustomEdge,
};

const Graph = ({ buttonClicked, setButtonClicked }) => {
    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

    useEffect(() => {
        if (!buttonClicked) return;

        const animateGraph = async () => {
            const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

            // Change first node to green
            setNodes((nds) =>
                nds.map((node) =>
                    node.id === NODE_IDS.BUYER
                        ? {
                            ...node,
                            style: {
                                ...node.style,
                                backgroundColor: 'rgba(0, 200, 0, 0.4)',
                                border: '1px solid #00FF00',
                            },
                        }
                        : node
                )
            );
            await delay(DELAY_DURATION);

            // Change edge color and label color to green
            setEdges((eds) =>
                eds.map((edge) =>
                    edge.id === EDGE_IDS.BUYER_TO_SOMMELIER
                        ? {
                            ...edge,
                            style: { ...edge.style, stroke: 'rgba(0, 200, 0, 0.4)' },
                            data: {
                                ...edge.data,
                                edgeColor: 'rgba(0, 200, 0, 0.4)',
                                labelColor: '#000000',
                                labelBackgroundColor: 'rgba(0, 200, 0, 0.4)',
                            },
                        }
                        : edge
                )
            );
            await delay(DELAY_DURATION);

            // Change second node to green
            setNodes((nds) =>
                nds.map((node) =>
                    node.id === NODE_IDS.SOMMELIER
                        ? {
                            ...node,
                            style: {
                                ...node.style,
                                backgroundColor: 'rgba(0, 200, 0, 0.4)',
                                border: '1px solid #00FF00',
                            },
                        }
                        : node
                )
            );
            await delay(DELAY_DURATION);

            // Reset nodes and edges to initial state
            setNodes((nds) =>
                nds.map((node) => ({
                    ...node,
                    style: initialNodes.find((n) => n.id === node.id).style,
                    position: node.position, // Ensure position remains unchanged
                }))
            );
            setEdges(initialEdges);

            // Reset buttonClicked state
            setButtonClicked(false);
        };

        animateGraph();
    }, [buttonClicked, setButtonClicked]);

    return (
        <div style={{ width: '100%', height: '100%' }}>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                proOptions={proOptions}
                edgeTypes={edgeTypes}
                fitView
            >
                <Controls />
            </ReactFlow>
        </div>
    );
};

// Wrapping with ReactFlowProvider
function FlowWithProvider(props) {
    return (
        <ReactFlowProvider>
            <Graph {...props} />
        </ReactFlowProvider>
    );
}

export default FlowWithProvider;
import React from 'react';
import { getBezierPath, EdgeLabelRenderer, BaseEdge } from '@xyflow/react';

const CustomEdge = ({
                        id,
                        sourceX,
                        sourceY,
                        targetX,
                        targetY,
                        sourcePosition,
                        targetPosition,
                        data,
                    }) => {
    const [edgePath, labelX, labelY] = getBezierPath({
        sourceX,
        sourceY,
        sourcePosition,
        targetX,
        targetY,
        targetPosition,
    });

    const edgeColor = data?.edgeColor || '#187ADC'; // Default edge color
    const labelColor = data?.labelColor || '#FFFFFF'; // Default label text color
    const labelBackgroundColor = data?.labelBackgroundColor || '#187ADC'; // Default label background color

    return (
        <>
            <svg style={{ position: 'absolute', top: 0, left: 0 }}>
                <defs>
                    <marker
                        id={`${id}-arrow-start`}
                        markerWidth="10"
                        markerHeight="10"
                        refX="1"
                        refY="5"
                        orient="auto"
                    >
                        <path d="M10,0 L0,5 L10,10 Z" fill={edgeColor} />
                    </marker>
                    <marker
                        id={`${id}-arrow-end`}
                        markerWidth="10"
                        markerHeight="10"
                        refX="9"
                        refY="5"
                        orient="auto"
                    >
                        <path d="M0,0 L10,5 L0,10 Z" fill={edgeColor} />
                    </marker>
                </defs>
            </svg>
            <BaseEdge
                id={id}
                path={edgePath}
                markerStart={`url(#${id}-arrow-start)`}
                markerEnd={`url(#${id}-arrow-end)`}
                style={{
                    stroke: edgeColor,
                    strokeWidth: 1,
                    cursor: 'pointer',
                }}
            />
            <EdgeLabelRenderer>
                <div
                    style={{
                        transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
                        backgroundColor: labelBackgroundColor,
                        width: 'fit-content',
                        color: labelColor,
                        padding: '2px 5px',
                        border: `1px solid ${labelColor}`,
                        borderRadius: '2px',
                        fontSize: '10px',
                        fontWeight: 'thin',
                        fontFamily: "'CiscoSansTT', sans-serif",
                        boxShadow: '0 1px 2px rgba(0, 0, 0, 0.2)',
                        whiteSpace: 'nowrap',
                    }}
                >
                    {data.label}
                </div>
            </EdgeLabelRenderer>
        </>
    );
};

export default CustomEdge;
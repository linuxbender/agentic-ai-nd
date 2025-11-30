"""
Visualize Agent Workflow Diagram using NetworkX - Demo Style
=============================================================

This script creates a professional network visualization similar to the
Uluru Cultural Center demo, showing all edges and data flow.
"""

import matplotlib.pyplot as plt
import networkx as nx
import re


def parse_mermaid_flowchart(filename):
    """Parse Mermaid flowchart and extract all nodes and edges."""
    nodes = {}
    edges = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Parse node definitions
        node_pattern = r'(\w+)\["([^"]+)"\]'
        for match in re.finditer(node_pattern, line):
            node_id = match.group(1)
            node_label = match.group(2).replace('<br/>', '\n')
            
            # Determine node type
            if 'Customer' in node_label:
                node_type = 'user'
            elif 'Tool:' in node_label or 'Tool' in node_label:
                node_type = 'tool'
            elif 'Agent' in node_label or 'Operations' in node_label:
                node_type = 'agent'
            else:
                node_type = 'default'
            
            nodes[node_id] = {
                'label': node_label,
                'type': node_type
            }
        
        # Parse edges (arrows)
        edge_pattern = r'(\w+)\s+-->\s*(?:\|([^|]+)\|)?\s*(\w+)'
        for match in re.finditer(edge_pattern, line):
            source = match.group(1)
            label = match.group(2).strip() if match.group(2) else ''
            target = match.group(3)
            edges.append((source, target, label))
    
    return nodes, edges


def create_diagram(title, nodes_dict, edges_list, output_file='agent_workflow_diagram.png'):
    """
    Create a professional diagram similar to demo.py style.
    
    Args:
        title: Diagram title
        nodes_dict: Dictionary of nodes with labels and types
        edges_list: List of tuples (source, target, label)
        output_file: Output filename
    """
    # Create directed graph
    graph = nx.DiGraph()
    
    # Add nodes
    nodes = list(nodes_dict.keys())
    graph.add_nodes_from(nodes)
    
    # Add edges
    edge_labels = {}
    for source, target, label in edges_list:
        if source in nodes and target in nodes:
            graph.add_edge(source, target)
            if label:
                edge_labels[(source, target)] = label
    
    # Extract node types and labels
    node_types = {node_id: data['type'] for node_id, data in nodes_dict.items()}
    node_labels = {node_id: data['label'] for node_id, data in nodes_dict.items()}
    
    # Create figure
    plt.figure(figsize=(16, 12))
    plt.title(title, fontsize=18, fontweight='bold', pad=25)
    
    # Use hierarchical layout for better flow visualization
    # Try different layouts based on graph structure
    if len(nodes) <= 8:
        pos = nx.spring_layout(graph, seed=42, k=2.5, iterations=100)
    else:
        pos = nx.kamada_kawai_layout(graph)
    
    # Adjust positions for better left-to-right or top-to-bottom flow
    x_values = [pos[node][0] for node in nodes]
    y_values = [pos[node][1] for node in nodes]
    min_x, max_x = min(x_values), max(x_values)
    min_y, max_y = min(y_values), max(y_values)
    
    # Normalize and scale positions
    for node in nodes:
        x, y = pos[node]
        normalized_x = (x - min_x) / (max_x - min_x + 1e-10)
        normalized_y = (y - min_y) / (max_y - min_y + 1e-10)
        pos[node] = (normalized_x * 6, normalized_y * 4)
    
    # Define colors, shapes, and sizes based on node types
    node_colors = []
    node_shapes = []
    node_sizes = []
    
    for node in nodes:
        node_type = node_types.get(node, 'default')
        
        if node_type == 'agent':
            node_colors.append("#6495ED")  # Cornflower Blue
            node_shapes.append('o')
            node_sizes.append(3500)
        elif node_type == 'tool':
            node_colors.append("#FFD700")  # Gold
            node_shapes.append('s')
            node_sizes.append(3200)
        elif node_type == 'user':
            node_colors.append("#FF6347")  # Tomato
            node_shapes.append('d')
            node_sizes.append(3800)
        elif node_type == 'data':
            node_colors.append("#90EE90")  # Light Green
            node_shapes.append('h')
            node_sizes.append(3000)
        else:
            node_colors.append("#C0C0C0")  # Silver
            node_shapes.append('p')
            node_sizes.append(2800)
    
    # Draw nodes individually to support different shapes
    for i, node in enumerate(nodes):
        nx.draw_networkx_nodes(graph, pos,
                             nodelist=[node],
                             node_color=[node_colors[i]],
                             node_shape=node_shapes[i],
                             node_size=node_sizes[i],
                             edgecolors='black',
                             linewidths=2.0,
                             alpha=0.9)
    
    # Draw edges with better styling
    nx.draw_networkx_edges(graph, pos,
                         edge_color="black",
                         arrowsize=30,
                         width=2.5,
                         alpha=0.7,
                         arrowstyle='-|>',
                         connectionstyle="arc3,rad=0.15")
    
    # Draw node labels with white background boxes
    for node, (x, y) in pos.items():
        label = node_labels[node]
        # Split long labels into multiple lines
        if '\n' in label:
            lines = label.split('\n')
            label = '\n'.join(lines[:2])  # Max 2 lines
        elif len(label) > 30:
            # Split at space closest to middle
            words = label.split()
            mid = len(label) // 2
            line1, line2 = [], []
            current_len = 0
            for word in words:
                if current_len < mid:
                    line1.append(word)
                    current_len += len(word) + 1
                else:
                    line2.append(word)
            label = ' '.join(line1) + '\n' + ' '.join(line2)
        
        plt.text(x, y, label,
                fontsize=10,
                ha='center',
                va='center',
                fontweight='bold',
                bbox=dict(facecolor='white',
                         alpha=0.85,
                         edgecolor='gray',
                         boxstyle='round,pad=0.6',
                         linewidth=1.5))
    
    # Draw edge labels
    if edge_labels:
        for edge, label in edge_labels.items():
            if edge[0] in pos and edge[1] in pos:
                x1, y1 = pos[edge[0]]
                x2, y2 = pos[edge[1]]
                x = (x1 + x2) / 2
                y = (y1 + y2) / 2 + 0.2
                plt.text(x, y, label,
                        fontsize=11,
                        ha='center',
                        va='center',
                        fontweight='bold',
                        color='darkblue',
                        bbox=dict(facecolor='lightyellow',
                                 alpha=0.95,
                                 edgecolor='blue',
                                 boxstyle='round,pad=0.4',
                                 linewidth=1.5))
    
    # Create legend
    legend_elements = [
        plt.Line2D([0], [0], marker='d', color='w', markerfacecolor="#FF6347", 
                   markersize=18, markeredgecolor='black', markeredgewidth=1.5,
                   label='Customer/User'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor="#6495ED", 
                   markersize=18, markeredgecolor='black', markeredgewidth=1.5,
                   label='Agent'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor="#FFD700", 
                   markersize=18, markeredgecolor='black', markeredgewidth=1.5,
                   label='Tool/Function'),
        plt.Line2D([0], [0], marker='h', color='w', markerfacecolor="#90EE90", 
                   markersize=18, markeredgecolor='black', markeredgewidth=1.5,
                   label='Data Component')
    ]
    legend = plt.legend(handles=legend_elements, 
                       loc='upper right', 
                       fontsize=13,
                       frameon=True,
                       fancybox=True,
                       shadow=True,
                       framealpha=0.95)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('black')
    legend.get_frame().set_linewidth(1.5)
    
    plt.axis("off")
    plt.tight_layout()
    
    # Save figure
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Diagram saved to: {output_file}")
    
    # Save PDF version
    pdf_file = output_file.replace('.png', '.pdf')
    plt.savefig(pdf_file, bbox_inches='tight', facecolor='white')
    print(f"✅ PDF version saved to: {pdf_file}")
    
    plt.close()


def main():
    """Main execution function."""
    print("=" * 70)
    print("Agent Workflow Diagram Visualizer - Demo Style")
    print("=" * 70)
    
    input_file = 'agent_workflow_diagram.mmd'
    output_file = 'agent_workflow_diagram.png'
    
    print(f"\n📖 Reading: {input_file}")
    nodes_dict, edges_list = parse_mermaid_flowchart(input_file)
    
    print(f"✓ Found {len(nodes_dict)} nodes")
    print(f"✓ Found {len(edges_list)} edges")
    
    # Print edges for verification
    print(f"\n📊 Edge connections:")
    for source, target, label in edges_list:
        label_str = f" ({label})" if label else ""
        print(f"  {source} → {target}{label_str}")
    
    print(f"\n🎨 Generating visualization...")
    create_diagram(
        "Multi-Agent Inventory & Sales System\nThe Beaver's Choice Paper Company",
        nodes_dict,
        edges_list,
        output_file
    )
    
    print(f"\n{'=' * 70}")
    print("✅ Visualization complete!")
    print(f"{'=' * 70}\n")


if __name__ == "__main__":
    main()

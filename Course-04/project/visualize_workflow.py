"""
Visualize Agent Workflow Diagram using NetworkX
================================================

This script parses the agent_workflow_diagram.mmd file and creates
a network visualization using NetworkX and Matplotlib.
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import re

def parse_mermaid_flowchart(filename):
    """
    Parse a Mermaid flowchart file and extract nodes and edges.
    
    Args:
        filename: Path to the .mmd file
        
    Returns:
        tuple: (nodes_dict, edges_list, subgraphs_dict)
    """
    nodes = {}
    edges = []
    subgraphs = {}
    current_subgraph = None
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract subgraph definitions
    subgraph_pattern = r'subgraph\s+(\w+)\["([^"]+)"\]'
    for match in re.finditer(subgraph_pattern, content):
        subgraph_id = match.group(1)
        subgraph_label = match.group(2)
        subgraphs[subgraph_id] = {
            'label': subgraph_label,
            'nodes': []
        }
    
    lines = content.split('\n')
    current_subgraph = None
    
    for line in lines:
        line = line.strip()
        
        # Detect subgraph start
        if line.startswith('subgraph'):
            match = re.match(r'subgraph\s+(\w+)', line)
            if match:
                current_subgraph = match.group(1)
            continue
        
        # Detect subgraph end
        if line == 'end' and current_subgraph:
            current_subgraph = None
            continue
        
        # Parse node definitions
        node_pattern = r'(\w+)\["([^"]+)"\]'
        for match in re.finditer(node_pattern, line):
            node_id = match.group(1)
            node_label = match.group(2).replace('<br/>', '\n')
            
            # Determine node type based on content
            if 'Tool:' in node_label:
                node_type = 'tool'
            elif 'Agent' in node_label or 'Operations' in node_label:
                node_type = 'agent'
            elif 'Customer' in node_label:
                node_type = 'customer'
            else:
                node_type = 'default'
            
            nodes[node_id] = {
                'label': node_label,
                'type': node_type,
                'subgraph': current_subgraph
            }
            
            if current_subgraph and current_subgraph in subgraphs:
                subgraphs[current_subgraph]['nodes'].append(node_id)
        
        # Parse edges (arrows)
        edge_pattern = r'(\w+)\s+-->\s*(?:\|([^|]+)\|)?\s*(\w+)'
        for match in re.finditer(edge_pattern, line):
            source = match.group(1)
            label = match.group(2) if match.group(2) else ''
            target = match.group(3)
            edges.append((source, target, label))
    
    return nodes, edges, subgraphs


def create_network_graph(nodes, edges, subgraphs):
    """
    Create a NetworkX graph from parsed Mermaid data.
    
    Args:
        nodes: Dictionary of nodes
        edges: List of edges
        subgraphs: Dictionary of subgraphs
        
    Returns:
        nx.DiGraph: Directed graph
    """
    G = nx.DiGraph()
    
    # Add nodes with attributes
    for node_id, node_data in nodes.items():
        G.add_node(node_id, **node_data)
    
    # Add edges
    for source, target, label in edges:
        if source in nodes and target in nodes:
            G.add_edge(source, target, label=label)
    
    return G


def visualize_graph(G, nodes, subgraphs, output_file='agent_workflow_diagram.png'):
    """
    Visualize the graph using Matplotlib.
    
    Args:
        G: NetworkX graph
        nodes: Dictionary of nodes
        subgraphs: Dictionary of subgraphs
        output_file: Output PNG filename
    """
    # Create figure with larger size for better readability
    fig, ax = plt.subplots(figsize=(20, 14))
    
    # Manual positioning for optimal hierarchical layout
    pos = {}
    
    # Customer at top center
    pos['Customer'] = (5, 10)
    
    # Orchestrator Agent below customer
    pos['OA'] = (5, 8.5)
    
    # Worker agents in a row below orchestrator
    worker_y = 5.5
    pos['IA'] = (1.5, worker_y)  # Inventory Agent
    pos['QA'] = (4.5, worker_y)  # Quote Agent  
    pos['SA'] = (7.5, worker_y)  # Sales Agent
    
    # Tools positioned below their respective agents
    tool_y_start = 3.5
    tool_spacing = 1.2
    
    # Inventory Agent Tools
    inv_tools = ['T1', 'T2']
    for i, tool_id in enumerate(inv_tools):
        if tool_id in nodes:
            pos[tool_id] = (1.5, tool_y_start - i * tool_spacing)
    
    # Quote Agent Tools
    quote_tools = ['T3', 'T4']
    for i, tool_id in enumerate(quote_tools):
        if tool_id in nodes:
            pos[tool_id] = (4.5, tool_y_start - i * tool_spacing)
    
    # Sales Agent Tools
    sales_tools = ['T5', 'T6']
    for i, tool_id in enumerate(sales_tools):
        if tool_id in nodes:
            pos[tool_id] = (7.5, tool_y_start - i * tool_spacing)
    
    # Define colors for different node types
    node_colors = {
        'customer': '#e1f5ff',
        'agent': '#ffe1e1',
        'tool': '#f0f0f0',
        'default': '#ffffff'
    }
    
    subgraph_colors = {
        'Orchestrator': '#ffe1e1',
        'InventoryAgent': '#e1ffe1',
        'QuoteAgent': '#fff5e1',
        'SalesAgent': '#f5e1ff'
    }
    
    # Subgraph box positions
    subgraph_boxes = {
        'Orchestrator': {'x': 3, 'y': 7.5, 'width': 4, 'height': 2},
        'InventoryAgent': {'x': 0, 'y': 1.5, 'width': 3, 'height': 4.5},
        'QuoteAgent': {'x': 3.2, 'y': 1.5, 'width': 2.8, 'height': 4.5},
        'SalesAgent': {'x': 6.2, 'y': 1.5, 'width': 2.8, 'height': 4.5}
    }
    
    # Draw subgraph backgrounds
    for sg_id, sg_data in subgraphs.items():
        if sg_id in subgraph_boxes and sg_data['nodes']:
            box = subgraph_boxes[sg_id]
            color = subgraph_colors.get(sg_id, '#f0f0f0')
            
            # Create rounded rectangle for subgraph
            rect = FancyBboxPatch(
                (box['x'], box['y']),
                box['width'], box['height'],
                boxstyle="round,pad=0.1",
                linewidth=2.5,
                edgecolor='#333',
                facecolor=color,
                alpha=0.25,
                zorder=0
            )
            ax.add_patch(rect)
            
            # Add subgraph label at top
            ax.text(box['x'] + box['width']/2, box['y'] + box['height'] + 0.15, 
                   sg_data['label'],
                   ha='center', va='bottom',
                   fontsize=11, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.4', 
                           facecolor='white', 
                           edgecolor='#333',
                           linewidth=2))
    
    # Draw edges with curved connections
    for edge in G.edges():
        source, target = edge
        if source in pos and target in pos:
            x1, y1 = pos[source]
            x2, y2 = pos[target]
            
            # Determine connection style based on relationship
            if source == 'Customer' or target == 'Customer':
                # Main flow lines - thicker
                linewidth = 3
                color = '#2563eb'
                alpha = 0.8
            elif source == 'OA' or target == 'OA':
                # Orchestrator connections - medium
                linewidth = 2.5
                color = '#dc2626'
                alpha = 0.7
            else:
                # Agent-Tool connections - thinner
                linewidth = 2
                color = '#666'
                alpha = 0.6
            
            # Draw arrow
            ax.annotate('',
                       xy=(x2, y2), xycoords='data',
                       xytext=(x1, y1), textcoords='data',
                       arrowprops=dict(
                           arrowstyle='->',
                           lw=linewidth,
                           color=color,
                           alpha=alpha,
                           connectionstyle='arc3,rad=0.2',
                           mutation_scale=25
                       ))
    
    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'label')
    for edge, label in edge_labels.items():
        if label and edge[0] in pos and edge[1] in pos:
            x1, y1 = pos[edge[0]]
            x2, y2 = pos[edge[1]]
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            
            ax.text(mid_x, mid_y, label,
                   ha='center', va='center',
                   fontsize=9,
                   fontweight='normal',
                   bbox=dict(boxstyle='round,pad=0.3', 
                           facecolor='white', 
                           edgecolor='#ddd',
                           alpha=0.9))
    
    # Draw nodes with improved styling
    for node_id, node_data in nodes.items():
        if node_id not in pos:
            continue
            
        x, y = pos[node_id]
        node_type = node_data['type']
        color = node_colors.get(node_type, '#ffffff')
        
        # Determine node size and style based on type
        if node_type == 'customer':
            width, height = 2.5, 0.8
            linewidth = 3
            fontsize = 12
            fontweight = 'bold'
        elif node_type == 'agent':
            width, height = 2, 0.7
            linewidth = 2.5
            fontsize = 11
            fontweight = 'bold'
        else:  # tool
            width, height = 2.5, 0.6
            linewidth = 1.5
            fontsize = 9
            fontweight = 'normal'
        
        # Draw node box with shadow effect
        # Shadow
        shadow = FancyBboxPatch(
            (x - width/2 + 0.05, y - height/2 - 0.05),
            width, height,
            boxstyle="round,pad=0.08",
            linewidth=0,
            facecolor='#00000020',
            zorder=9
        )
        ax.add_patch(shadow)
        
        # Main box
        rect = FancyBboxPatch(
            (x - width/2, y - height/2),
            width, height,
            boxstyle="round,pad=0.08",
            linewidth=linewidth,
            edgecolor='#333',
            facecolor=color,
            zorder=10
        )
        ax.add_patch(rect)
        
        # Add node label with better text wrapping
        label_lines = node_data['label'].split('\n')
        max_lines = 4 if node_type == 'tool' else 3
        
        for i, line in enumerate(label_lines[:max_lines]):
            offset = (i - len(label_lines[:max_lines])/2 + 0.5) * 0.18
            ax.text(x, y + offset, line,
                   ha='center', va='center',
                   fontsize=fontsize,
                   fontweight=fontweight,
                   color='#1f2937',
                   zorder=11)
    
    # Create legend with better styling
    legend_elements = [
        mpatches.Patch(facecolor='#e1f5ff', edgecolor='#333', linewidth=2, label='Customer'),
        mpatches.Patch(facecolor='#ffe1e1', edgecolor='#333', linewidth=2, label='Orchestrator Agent'),
        mpatches.Patch(facecolor='#e1ffe1', edgecolor='#333', linewidth=2, label='Inventory Agent'),
        mpatches.Patch(facecolor='#fff5e1', edgecolor='#333', linewidth=2, label='Quote Agent'),
        mpatches.Patch(facecolor='#f5e1ff', edgecolor='#333', linewidth=2, label='Sales Agent'),
        mpatches.Patch(facecolor='#f0f0f0', edgecolor='#666', linewidth=1.5, label='Tools')
    ]
    legend = ax.legend(handles=legend_elements, loc='upper left', fontsize=10,
                      frameon=True, fancybox=True, shadow=True,
                      title='Components', title_fontsize=11)
    legend.get_frame().set_facecolor('#ffffff')
    legend.get_frame().set_alpha(0.95)
    
    # Set title with better styling
    ax.text(5, 11.2, 'Multi-Agent Inventory & Sales System',
           ha='center', va='center',
           fontsize=18, fontweight='bold',
           color='#1f2937')
    ax.text(5, 10.7, 'Workflow Architecture - The Beaver\'s Choice Paper Company',
           ha='center', va='center',
           fontsize=12, fontweight='normal',
           color='#4b5563', style='italic')
    
    # Remove axes and set limits
    ax.set_xlim(-0.5, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Add grid background (subtle)
    ax.set_facecolor('#f9fafb')
    
    # Save figure
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Diagram saved to: {output_file}")
    
    # Also save as high-res PDF
    pdf_file = output_file.replace('.png', '.pdf')
    plt.savefig(pdf_file, bbox_inches='tight', facecolor='white')
    print(f"✅ PDF version saved to: {pdf_file}")
    
    plt.close()


def main():
    """Main execution function."""
    print("=" * 60)
    print("Agent Workflow Diagram Visualizer")
    print("=" * 60)
    
    input_file = 'agent_workflow_diagram.mmd'
    output_file = 'agent_workflow_diagram.png'
    
    print(f"\n📖 Reading: {input_file}")
    nodes, edges, subgraphs = parse_mermaid_flowchart(input_file)
    
    print(f"✓ Found {len(nodes)} nodes")
    print(f"✓ Found {len(edges)} edges")
    print(f"✓ Found {len(subgraphs)} subgraphs")
    
    print(f"\n🔨 Creating network graph...")
    G = create_network_graph(nodes, edges, subgraphs)
    
    print(f"✓ Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    
    print(f"\n🎨 Generating visualization...")
    visualize_graph(G, nodes, subgraphs, output_file)
    
    print(f"\n{'=' * 60}")
    print("✅ Visualization complete!")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()

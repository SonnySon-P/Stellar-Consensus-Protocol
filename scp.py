import random
import pygame
import numpy as np

width, height = 1000, 800
margin = 50

nodes_number = 90
communication_radius = 200
step_interval = 2
accept_threshold = 2/3
confirm_threshold = 3/4

background_color = (18, 20, 24)
edge_color = (200, 200, 200)
text_color = (230, 230, 230)
idle_color = (120, 120, 120)
vote0_color = (52, 152, 219)
vote1_color = (243, 156, 18)
confirm0_color = (155, 89, 182)
confirm1_color = (46, 204, 113)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simplified SCP Simulation")
font = pygame.font.SysFont("consolas", 16)
clock = pygame.time.Clock()

def distance(position1, position2):
    return np.linalg.norm(position1 - position2)

class Node:
    def __init__(self, id):
        self.id = id
        self.position = np.array([random.uniform(margin, width - margin), random.uniform(margin + 50, height - margin)], dtype = float)
        self.communication_radius = communication_radius
        self.neighbors = []
        self.trust = set()
        self.value = random.choice([0, 1])
        self.accepted = False
        self.confirmed = False

    def build_neighbor(self, nodes):
        self.neighbors.clear()
        for other_node in nodes:
            if self.id != other_node.id:
                if distance(self.position, other_node.position) <= self.communication_radius:
                    self.neighbors.append(other_node.id)
                    self.trust.add(other_node.id)

    def draw(self, node_dictionary):
        for neighbor in self.neighbors:
            neighbor_position = node_dictionary[neighbor]
            pygame.draw.line(screen, (*edge_color, 50), self.position, neighbor_position.position, 1)
        
        if self.confirmed:
            if self.value == 0:
                color = confirm0_color
            else:
                color = confirm1_color
        elif self.accepted:
            if self.value == 0:
                color = vote0_color
            else:
                color = vote1_color
        else:
            color = idle_color

        pygame.draw.circle(screen, color, (self.position[0], self.position[1]), 6)

def step(nodes):
    update_values = [node.value for node in nodes]
    update_accepted = [node.accepted for node in nodes]
    update_confirmed = [node.confirmed for node in nodes]

    for i, node in enumerate(nodes):
        if node.confirmed:
            continue

        trust = list(node.trust)
        if not trust:
            continue

        votes_0 = 0
        votes_1 = 0
        accepted_0 = 0
        accepted_1 = 0
        confirmed_0 = 0
        confirmed_1 = 0

        for id in trust:
            if id >= len(nodes):
                continue

            trust_node = nodes[id]
            if trust_node.value == 0:
                votes_0 = votes_0 + 1
            elif trust_node.value == 1:
                votes_1 = votes_1 + 1

            if trust_node.accepted:
                if trust_node.value == 0:
                    accepted_0 = accepted_0 + 1
                elif trust_node.value == 1:
                    accepted_1 = accepted_1 + 1

            if trust_node.confirmed:
                if trust_node.value == 0:
                    confirmed_0 = confirmed_0 + 1
                elif trust_node.value == 1:
                    confirmed_1 = confirmed_1 + 1

        trust_quantity = len(trust)
        support_vote_0 = votes_0 / trust_quantity
        support_vote_1 = votes_1 / trust_quantity

        if not node.accepted and not node.confirmed:
            if votes_0 > votes_1 and support_vote_0 >= accept_threshold:
                update_values[i] = 0
                update_accepted[i] = True
            elif votes_1 > votes_0 and support_vote_1 >= accept_threshold:
                update_values[i] = 1
                update_accepted[i] = True
        elif node.accepted and not node.confirmed:
            if node.value == 0 and support_vote_0 >= confirm_threshold:
                update_values[i] = 0
                update_confirmed[i] = True
            elif node.value == 1 and support_vote_1 >= confirm_threshold:
                update_confirmed[i] = True
            elif node.value == 0 and support_vote_1 >= confirm_threshold:
                update_values[i] = 1
                update_accepted[i] = True
            elif node.value == 1 and support_vote_0 >= confirm_threshold:
                update_values[i] = 0
                update_accepted[i] = True

    for i, node in enumerate(nodes):
        node.value = update_values[i]
        node.accepted = update_accepted[i]
        node.confirmed = update_confirmed[i]

def main():
    nodes = [Node(i + 1) for i in range(nodes_number)]
    for node in nodes:
        node.build_neighbor(nodes)

    node_dictionary = {node.id: node for node in nodes}

    screen.fill(background_color)
    for node in nodes:
        node.draw(node_dictionary)
    pygame.display.flip()

    frame = 0
    step_count = 0
    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:
            frame = frame + 1
            if frame % step_interval == 0:
                step(nodes)
                step_count = step_count + 1

            screen.fill(background_color)
            for node in nodes:
                node.draw(node_dictionary)

            c0 = sum(1 for node in nodes if node.confirmed and node.value == 0)
            c1 = sum(1 for node in nodes if node.confirmed and node.value == 1)
            if all(node.confirmed for node in nodes):
                s = "finish"
                paused = True
            else:
                s = "run"
            lines = [
                f"Nodes Number: {len(nodes)}",
                f"Confirmed 1 (green): {c1}   Confirmed 0 (purple): {c0}",
                f"Paused: {paused}   Steps: {step_count}   Consensus State: {s}",
                f"Keys: [Space] = Pause / Run"
            ]
            y = 10
            for line in lines:
                text = font.render(line, True, text_color)
                screen.blit(text, (10, y))
                y = y + 20

            pygame.display.flip()

            clock.tick(1)

    pygame.quit()

if __name__ == "__main__":
    main()

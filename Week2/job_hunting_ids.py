class JobNode:
    def __init__(self, job_title, is_suitable, children=None):
        self.job_title = job_title
        self.is_suitable = is_suitable
        self.children = []


def job_hunting_ids_search(root, max_depth):
    def find_job_at_depth(node, current_depth):
        if current_depth == 0:
            return (node.is_suitable, node.job_title) if node else (False, None)

        if node:
            for child in node.children:
                found, job_title = find_job_at_depth(child, current_depth - 1)
                if found:
                    return True, job_title
        return False, None

    for depth in range(max_depth + 1):
        found, job_title = find_job_at_depth(root, depth)
        if found:
            print(f"Suitable job found at depth {depth}: {job_title}")
            return True
    return False


if __name__ == "__main__":
    root = JobNode('CEO', False)

    node1 = JobNode("Senior Developer", False)
    node2 = JobNode("Project Manager", False)
    node3 = JobNode("Quality Assurance Engineer", False)
    root.children = [node1, node2, node3]

    node1.children = [JobNode("Lead Software Engineer", True), JobNode("Senior Software Engineer", True)]
    node2.children = [JobNode("Product Manager", False), JobNode("Program Manager", False)]
    node3.children = [JobNode("QA Lead", False), JobNode("QA Analyst", False)]

    node1.children[0].children = [JobNode("Principal Engineer", True), JobNode("Engineering Manager", True)]
    node1.children[1].children = [JobNode("Staff Engineer", True)]
    node2.children[0].children = [JobNode("Senior Product Manager", False)]
    node2.children[1].children = [JobNode("Technical Program Manager", False)]
    node3.children[0].children = [JobNode("Senior QA Lead", False)]
    node3.children[1].children = [JobNode("QA Specialist", False)]

    for child in node1.children[0].children:
        child.children = [JobNode("VP of Engineering", True)]
    for child in node1.children[1].children:
        child.children = [JobNode("Engineering Director", True)]
    for child in node2.children:
        child.children = [JobNode("Director of Product Management", False)]
    for child in node3.children:
        child.children = [JobNode("QA Director", False)]

    max_depth = 4

    # Perform IDS to find if there's a suitable job
    found = job_hunting_ids_search(root, max_depth)
    if not found:
        print("No suitable job found.")

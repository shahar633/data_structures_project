from AVLTree import AVLTree
import random


def print_tree(root):
    """Print the tree in a centered layout with children under each parent."""
    if root is None or not root.is_real_node():
        print("(empty)")
        return

    def label(node):
        return f"{node.key}:{node.value}"

    def build(node):
        text = label(node)
        text_width = len(text)

        if not node.left.is_real_node() and not node.right.is_real_node():
            return [text], text_width, 1, text_width // 2

        if not node.right.is_real_node():
            lines, width, height, middle = build(node.left)
            first_line = " " * (middle + 1) + " " * (width - middle - 1) + text
            second_line = " " * middle + "/" + " " * (width - middle - 1 + text_width)
            shifted_lines = [line + " " * text_width for line in lines]
            return [first_line, second_line] + shifted_lines, width + text_width, height + 2, width + text_width // 2

        if not node.left.is_real_node():
            lines, width, height, middle = build(node.right)
            first_line = text + " " * middle + " " * (width - middle)
            second_line = " " * text_width + "\\" + " " * (width - middle - 1)
            shifted_lines = [" " * text_width + line for line in lines]
            return [first_line, second_line] + shifted_lines, width + text_width, height + 2, text_width // 2

        left_lines, left_width, left_height, left_middle = build(node.left)
        right_lines, right_width, right_height, right_middle = build(node.right)

        first_line = (
            " " * (left_middle + 1)
            + " " * (left_width - left_middle - 1)
            + text
            + " " * right_middle
            + " " * (right_width - right_middle)
        )
        second_line = (
            " " * left_middle
            + "/"
            + " " * (left_width - left_middle - 1 + text_width + right_middle)
            + "\\"
            + " " * (right_width - right_middle - 1)
        )

        if left_height < right_height:
            left_lines += [" " * left_width] * (right_height - left_height)
        elif right_height < left_height:
            right_lines += [" " * right_width] * (left_height - right_height)

        merged_lines = [
            left_line + " " * text_width + right_line
            for left_line, right_line in zip(left_lines, right_lines)
        ]
        return [first_line, second_line] + merged_lines, left_width + text_width + right_width, max(left_height, right_height) + 2, left_width + text_width // 2

    for line in build(root)[0]:
        print(line)


def show(title, tree_obj):
    print(f"\n=== {title} ===")
    print_tree(tree_obj.get_root())


def dump_tree(node, depth=0):
    if node is None or not node.is_real_node():
        return

    parent_key = None
    if node.parent is not None and node.parent.is_real_node():
        parent_key = node.parent.key

    print("  " * depth + f"{node.key} (parent={parent_key}, height={node.height})")
    dump_tree(node.left, depth + 1)
    dump_tree(node.right, depth + 1)


def run_case(title, tree, delete_key):
    print(f"\n=== {title} ===")
    print("Before delete:")
    dump_tree(tree.get_root())
    print_tree(tree.get_root())

    node, _ = tree.search(delete_key)
    try:
        tree.delete(node)
        print(f"After deleting {delete_key}:")
        dump_tree(tree.get_root())
        print_tree(tree.get_root())
    except Exception as exc:
        print(f"Delete raised {type(exc).__name__}: {exc}")
        print("Tree after exception (if still usable):")
        try:
            dump_tree(tree.get_root())
            print_tree(tree.get_root())
        except Exception as inner_exc:
            print(f"Could not print tree after exception: {type(inner_exc).__name__}: {inner_exc}")


def collect_height_mismatches(node, result=None):
    if result is None:
        result = []
    if node is None or not node.is_real_node():
        return result

    expected = 1 + max(
        -1 if not node.left.is_real_node() else collect_expected_height(node.left),
        -1 if not node.right.is_real_node() else collect_expected_height(node.right),
    )
    if node.height != expected:
        result.append((node.key, node.height, expected))

    collect_height_mismatches(node.left, result)
    collect_height_mismatches(node.right, result)
    return result


def collect_expected_height(node):
    if node is None or not node.is_real_node():
        return -1
    return 1 + max(collect_expected_height(node.left), collect_expected_height(node.right))


def expected_search_time_from_root(tree, key):
    root = tree.get_root()
    if root is None:
        return 1, None

    cur = root
    steps = 0
    while cur.is_real_node():
        if key == cur.key:
            return steps + 1, cur
        steps += 1
        cur = cur.left if key < cur.key else cur.right
    return steps + 1, None


def verify_tree(tree, active_keys, context):
    problems = []

    current_list = tree.avl_to_list()
    expected_list = [(key, str(key)) for key in sorted(active_keys)]
    if current_list != expected_list:
        problems.append(("avl_to_list", current_list, expected_list))

    size_value = tree.size()
    if size_value != len(active_keys):
        problems.append(("size", size_value, len(active_keys)))

    root = tree.get_root()
    expected_height = collect_expected_height(root)
    reported_height = tree.get_height()
    if reported_height != expected_height:
        problems.append(("height", reported_height, expected_height))

    if root is None:
        if active_keys:
            problems.append(("root", None, "non-empty tree"))
    else:
        if root.parent is not None and root.parent.is_real_node():
            problems.append(("root_parent", root.parent.key, None))

    for key in active_keys:
        found, search_time = tree.search(key)
        expected_time, expected_node = expected_search_time_from_root(tree, key)
        if found is None or found.key != key:
            problems.append((f"search_found_{key}", None if found is None else found.key, key))
        if search_time != expected_time:
            problems.append((f"search_time_{key}", search_time, expected_time))
        if expected_node is not None and found is not expected_node:
            problems.append((f"search_node_identity_{key}", found.key if found else None, expected_node.key))

    missing_candidates = [-999999, -123, 999999]
    for key in missing_candidates:
        if key in active_keys:
            continue
        found, search_time = tree.search(key)
        expected_time, expected_node = expected_search_time_from_root(tree, key)
        if found is not None:
            problems.append((f"missing_search_found_{key}", found.key, None))
        if search_time != expected_time:
            problems.append((f"missing_search_time_{key}", search_time, expected_time))
        if expected_node is not None:
            problems.append((f"missing_search_expected_node_{key}", expected_node.key, None))

    if problems:
        print(f"\n!!! CHECK FAILED: {context} !!!")
        print("Problems:")
        for problem in problems:
            print("  ", problem)
        print("Tree dump:")
        dump_tree(tree.get_root())
        print("Pretty tree:")
        print_tree(tree.get_root())
        return False

    return True


def run_insert(tree, active_keys, key):
    expected_time, _ = expected_search_time_from_root(tree, key)
    node, search_time, rotations, height_changes = tree.insert(key, str(key))
    active_keys.add(key)
    print(f"insert({key}) -> node={node.key}, search_time={search_time}, rotations={rotations}, height_changes={height_changes}")
    print_tree(tree.get_root())
    if search_time != expected_time:
        print(f"  [search_time mismatch] got {search_time}, expected {expected_time}")
    return verify_tree(tree, active_keys, f"after insert {key}")


def run_delete(tree, active_keys, key):
    node, found_time = tree.search(key)
    print(f"search({key}) before delete -> found={None if node is None else node.key}, search_time={found_time}")
    if node is None:
        print(f"delete({key}) skipped because the key is missing")
        return verify_tree(tree, active_keys, f"after skipped delete {key}")

    try:
        tree.delete(node)
        active_keys.remove(key)
        print(f"delete({key}) -> ok")
    except Exception as exc:
        print(f"delete({key}) -> raised {type(exc).__name__}: {exc}")
        print_tree(tree.get_root())
        return False

    print_tree(tree.get_root())
    return verify_tree(tree, active_keys, f"after delete {key}")


def stress_tree(label, is_avl, insert_keys, delete_keys, extra_search_keys):
    print(f"\n================ {label} ================")
    tree = AVLTree(is_avl)
    active_keys = set()

    print(f"mode: {'AVL' if is_avl else 'BST'}")
    print(f"initial root={tree.get_root()}, size={tree.size()}, height={tree.get_height()}")
    verify_tree(tree, active_keys, f"initial state {label}")

    for key in insert_keys:
        if key in active_keys:
            continue
        if not run_insert(tree, active_keys, key):
            return False

    for key in extra_search_keys:
        found, search_time = tree.search(key)
        expected_time, _ = expected_search_time_from_root(tree, key)
        print(f"search({key}) -> found={None if found is None else found.key}, search_time={search_time}, expected={expected_time}")
        if search_time != expected_time:
            print(f"  [search_time mismatch for {key}]")
            print_tree(tree.get_root())

    for key in delete_keys:
        if key not in active_keys:
            continue
        if not run_delete(tree, active_keys, key):
            return False

    print(f"final size={tree.size()}, final height={tree.get_height()}, final list={tree.avl_to_list()}")
    return verify_tree(tree, active_keys, f"final state {label}")


def main():
   
    random.seed(7)

    cases = [
        (
            "AVL zig-zag pressure",
            True,
            [40, 20, 60, 10, 30, 50, 70, 25, 27, 26, 24, 23, 22, 21, 65, 75, 80, 5, 15, 35, 45, 55],
            [26, 27, 25, 24, 23, 22, 21, 30, 20, 70, 65, 75, 80, 60, 50, 40, 10, 15, 5, 35, 45, 55],
            [-5, 0, 1, 17, 19, 44, 46, 100, 999],
        ),
        (
            "AVL two-children delete pressure",
            True,
            [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 5],
            [20, 30, 70, 50, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 5],
            [-1, 6, 11, 29, 41, 52, 1000],
        ),
        (
            "BST deep chain pressure",
            False,
            list(range(1, 18)),
            [2, 4, 6, 8, 10, 12, 14, 16, 1, 3, 5, 7, 9],
            [0, 11, 17, 18, 100],
        ),
    ]

    overall_ok = True
    for label, is_avl, insert_keys, delete_keys, search_keys in cases:
        ok = stress_tree(label, is_avl, insert_keys, delete_keys, search_keys)
        overall_ok = overall_ok and ok

    for trial in range(3):
        keys = list(range(trial * 20, trial * 20 + 14))
        random.shuffle(keys)
        delete_keys = keys[:]
        random.shuffle(delete_keys)
        ok = stress_tree(
            f"random AVL trial {trial + 1}",
            True,
            keys,
            delete_keys,
            [trial * 20 - 1, trial * 20 + 14, trial * 20 + 100],
        )
        overall_ok = overall_ok and ok

    print("\nOVERALL RESULT:", "PASS" if overall_ok else "FAIL")


if __name__ == "__main__":
    main()

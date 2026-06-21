from AVLTree import AVLTree
import random as Random


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


def main():
    T = AVLTree(True)
    rotations = 0
    print(T.insert(46, "46")[2])
    show("After inserting 46", T)
    print(T.insert(17, "17")[2])
    show("After inserting 17", T)
    print(T.insert(18, "18")[2])
    show("After inserting 18", T)
    print(T.insert(19, "19")[2])
    show("After inserting 19", T)
    print(T.insert(20, "20")[2])
    show("After inserting 20", T)
    print(T.insert(21, "21")[2])
    show("After inserting 21", T)
    print(T.insert(22, "22")[2])
    show("After inserting 22", T)
    print(T.insert(23, "23")[2])
    show("After inserting 23", T)


if __name__ == "__main__":
    main()

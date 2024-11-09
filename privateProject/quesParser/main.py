from collections import deque


def bfs(grid, start_x, start_y, visited):
    queue = deque([(start_x, start_y)])
    visited[start_x][start_y] = True

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右，下，左，上

    while queue:
        x, y = queue.popleft()

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and not visited[nx][ny] and grid[nx][ny] == 1:
                visited[nx][ny] = True
                queue.append((nx, ny))


def find_number_of_islands(grid):
    if not grid:
        return 0

    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    island_count = 0

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1 and not visited[i][j]:
                bfs(grid, i, j, visited)
                island_count += 1

    return island_count


# 示例网格
if __name__ == '__main__':
    grid = [
        [1, 1, 0, 0, 0],
        [1, 0, 0, 1, 1],
        [0, 0, 0, 0, 1],
        [0, 1, 1, 0, 0]
    ]
    print(find_number_of_islands(grid))  # 输出连接区域的数量

import subprocess  
import os

# 定义常量  
GITLAB_PATH = '/data/app/gitlab'  
CONTAINER_NAME = 'gitlab'
REMOTE_HOST = '116.204.14.247'
REMOTE_USER = 'root'
REMOTE_PORT = 2222  
REMOTE_PATH = '/data/app/gitlab/data'  

# 同步数据  
def sync_data():  
    try:  
        rsync_command = [  
            'rsync', '-azP', '--delete',  
            f'-e "ssh -p {REMOTE_PORT}"',  
            f'{REMOTE_USER}@{REMOTE_HOST}:{REMOTE_PATH}',  
            GITLAB_PATH  
        ]  
        subprocess.run(rsync_command, check=True)  
        print("数据同步成功。")  
    except subprocess.CalledProcessError as e:  
        print(f"数据同步失败: {e}")  

# 重新配置GitLab  
def reconfigure_gitlab():  
    try:  
        docker_command = ['docker', 'exec', CONTAINER_NAME, 'gitlab-ctl', 'reconfigure']  
        subprocess.run(docker_command, check=True)  
        print("GitLab配置重新加载成功。")  
    except subprocess.CalledProcessError as e:  
        print(f"GitLab配置重新加载失败: {e}")  

# 重新启动GitLab容器  
def restart_container():  
    try:  
        docker_compose_command = ['docker-compose', 'restart', CONTAINER_NAME]  
        subprocess.run(docker_compose_command, check=True)  
        print("GitLab容器重启成功。")  
    except subprocess.CalledProcessError as e:  
        print(f"GitLab容器重启失败: {e}")  

# 主执行流程  
def main():  
    os.chdir(GITLAB_PATH)  
    sync_data()  
    reconfigure_gitlab()  
    restart_container()  

if __name__ == "__main__":  
    main()

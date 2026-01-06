import asyncio
import shutil
from camunda_orchestration_sdk.runtime.job_worker import JobContext

async def simulate_subprocess_work(job: JobContext, duration: float = 5.0):
    """
    Simulates a realistic CPU-bound workload by spawning a subprocess.
    
    This allows the operating system to schedule the heavy work on a different CPU core,
    bypassing the Python GIL. This is ideal for tasks like video transcoding,
    image processing, or heavy compression.
    """
    print(f"Starting subprocess work for job {job.job_key}")

    # Check for ffmpeg, fallback to gzip if not found
    if shutil.which("ffmpeg"):
        # Generate video noise (CPU intensive)
        # -f lavfi -i testsrc... generates a test video pattern
        # -f null - discards the output
        cmd = [
            "ffmpeg",
            "-f", "lavfi",
            "-i", f"testsrc=duration={duration}:size=1920x1080:rate=30",
            "-f", "null",
            "-"
        ]
        tool_name = "ffmpeg"
    else:
        # Fallback: gzip compression of random data
        # We use a shell command to pipe urandom into gzip
        # This burns CPU on compression
        cmd = [
            "bash", "-c",
            f"dd if=/dev/urandom bs=1024 count={int(duration * 2000)} 2>/dev/null | gzip -9 > /dev/null"
        ]
        tool_name = "gzip"

    print(f"Delegating work to {tool_name}...")
    
    # Run the command asynchronously
    # The Python event loop stays free to handle heartbeats/polling
    # while the OS schedules the subprocess on another core.
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )
    
    await process.wait()
    print(f"Completed {tool_name} work for job {job.job_key}")
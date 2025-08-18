import os
import logging
from instance_solver import create_model_from_instance, solve_qbf_model, log_results
from instance_io import read_max_sc_qbf_instance 

def setup_logger(name, log_file, level=logging.INFO):
    """Function to set up a logger that writes to a specific file."""
    
    # To prevent loggers from propagating messages to the root logger,
    # we use a handler specific to this logger.
    handler = logging.FileHandler(log_file, mode='a') # 'a' for append
    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers if they already exist
    if not logger.handlers:
        logger.addHandler(handler)
        
        # Optionally, add a handler to also print to console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(stream_handler)

    return logger

def main():
    # --- 1. Configuration ---
    # Map each generation/directory to its specific summary log file.
    log_config = {
        'gen1': 'summary_results1.log',
        'gen2': 'summary_results2.log',
        'gen3': 'summary_results3.log',
    }
    
    base_instance_dir = "data/instances"
    
    # Directory to store detailed solver logs, now structured by generation.
    base_solver_log_dir = "solver_logs"
    os.makedirs(base_solver_log_dir, exist_ok=True)

    # --- 2. Processing Loop for Each Generation ---
    for gen_name, summary_log_file in log_config.items():
        
        # Set up a dedicated logger for this generation
        logger = setup_logger(gen_name, summary_log_file)
        logger.info(f"--- Starting new batch for generation: {gen_name} ---")

        instance_dir = os.path.join(base_instance_dir, gen_name)
        
        # Create a dedicated subdirectory for this generation's solver logs
        solver_log_dir = os.path.join(base_solver_log_dir, gen_name)
        os.makedirs(solver_log_dir, exist_ok=True)
        
        if not os.path.isdir(instance_dir):
            logger.warning(f"Instance directory not found, skipping: {instance_dir}")
            continue

        instance_files = [f for f in os.listdir(instance_dir) if f.endswith('.txt')]

        for instance_file in instance_files:
            instance_path = os.path.join(instance_dir, instance_file)
            instance_name = os.path.basename(instance_path)
            
            logger.info(f"Processing instance: {instance_name}")
            
            try:
                # Step 1: Read the instance data
                instance = read_max_sc_qbf_instance(instance_path)

                # Step 2: Create the Pyomo model
                model = create_model_from_instance(instance)

                # Step 3: Solve and save the detailed solver log
                solver_log_path = os.path.join(solver_log_dir, f"{instance_name}.log")
                results = solve_qbf_model(model, logfile=solver_log_path)

                # Step 4: Log summary using the dedicated logger for this generation
                log_results(logger, results, instance, instance_name)

            except Exception as e:
                logger.error(f"Failed to process instance {instance_name}. Error: {e}", exc_info=True)
    
    print("\nFinished processing all generations.")

if __name__ == "__main__":
    main()


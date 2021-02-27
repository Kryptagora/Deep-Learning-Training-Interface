import torch
import torch.nn as nn
#matplotlib.use('TkAgg')
from types import SimpleNamespace
import sys
import time
sys.path.append('..')

from utils.dataloader import load_data
from utils.check_filename import check_filename
from architecture.CNN import CNN

def train(main_window=None):
    try:
        args = SimpleNamespace(batch_size=main_window.NetworkFrame.bs.get(), test_batch_size=100, epochs=main_window.NetworkFrame.epochs.get(),
                           lr=main_window.NetworkFrame.lr.get(), momentum=main_window.NetworkFrame.momentum.get(), seed=1, log_interval=100)
    except:
        main_window.set_warn('Invalid Hyperparameters!')
        return None


    suc, err = check_filename(str(main_window.NetworkFrame.modelname.get()))
    if suc is False:
        main_window.set_warn(err)
        return None
    else:
        save_model_as = err
        main_window.set_info(f'Model will be saved as {save_model_as}')


    # some considerations
    main_window.ConsoleFrame.delete_text()
    main_window.NetworkFrame.reset_params()

    # args = SimpleNamespace(batch_size=500, test_batch_size=100, epochs=1,
    #                        lr=0.001, momentum=0.5, seed=1, log_interval=100)

    main_window.ConsoleFrame.push_text('Loading Data...\n')
    train_loader, test_loader = load_data(batch_size=args.batch_size, root_folder='data', dataset=main_window.NetworkFrame.dataset_select.get())
    torch.manual_seed(args.seed)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    main_window.ConsoleFrame.device_text.set(device)

    main_window.ConsoleFrame.push_text('Loading Model...\n')
    model = CNN(out_labels=62).to(device)

    # Loss and optimize
    main_window.ConsoleFrame.push_text('Loading Optimizer...\n')
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    total_step = len(train_loader)
    main_window.ConsoleFrame.spawn_progressbar(len(train_loader))

    # Restarting Animation
    main_window.AnimationFrame.stop_animation()

    # update frame every 60 seconds
    t0 = time.time()
    t1 = t0
    main_window.ConsoleFrame.push_text('Done! Training Start...\n---------------------\n')
    for epoch in range(args.epochs):
        main_window.ConsoleFrame.delete_text()
        main_window.ConsoleFrame.epoch_text.set(f"Epoch {epoch+1} of {args.epochs}: ")
        main_window.ConsoleFrame.pb["value"] = 0

        for i, (images, labels) in enumerate(train_loader):
            # when training is aborted
            if main_window.NetworkFrame.stop_train:
                main_window.ConsoleFrame.delete_text()
                main_window.NetworkFrame.stop_train = False
                main_window.NetworkFrame.train_button.config(state='normal')
                main_window.ConsoleFrame.push_text('Training Interrupted!\n')
                main_window.set_info('Training Interrupted.')
                return None

            elif main_window.NetworkFrame.stop_save:
                main_window.ConsoleFrame.push_text('Training stoped early!\n')
                main_window.set_info('Training stopped early, time for the test set.')
                break

            images = images.to(device)
            labels = labels.to(device)

            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)

            # Backprop and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # 60 FPS
            if time.time() - t0 > 1/60:
                main_window.ConsoleFrame.frame.update()
                main_window.ConsoleFrame.pb["value"] = i

                # Animations
                main_window.AnimationFrame.ys.append(round(loss.item(), 3))
                main_window.AnimationFrame.xs.append(time.time())

                t0 = time.time()

            # lowewr fps for plotting
            if time.time() - t1 > 1/20:
                main_window.AnimationFrame.animate()
                t1=time.time()


            if (i+1) % 50 == 0:
                main_window.ConsoleFrame.push_text(f'Current Loss: {round(loss.item(), 3)}\n')
                main_window.AnimationFrame.ys_global.append(round(loss.item(), 2))
                main_window.AnimationFrame.xs_global.append(time.time())
                main_window.AnimationFrame.animate2()

    main_window.ConsoleFrame.delete_text()
    main_window.ConsoleFrame.push_text('Training Done! Testing Model...\n')
    main_window.ConsoleFrame.pb["value"] = 0
    main_window.ConsoleFrame.change_max_value(len(test_loader))
    main_window.ConsoleFrame.epoch_text.set(f"Testing Network...")

    # Test the model
    model.eval()  # eval mode (batchnorm uses moving mean/variance instead of mini-batch mean/variance)
    with torch.no_grad():
        correct = 0
        total = 0
        for i ,(images, labels) in enumerate(test_loader):
            if main_window.NetworkFrame.stop_train:
                main_window.ConsoleFrame.delete_text()
                main_window.NetworkFrame.stop_train = False
                main_window.NetworkFrame.train_button.config(state='normal')
                main_window.ConsoleFrame.push_text('Testing Interrupted!\n')
                return None

            # update window
            if time.time() - t0 > 1/60:
                main_window.ConsoleFrame.frame.update()
                main_window.ConsoleFrame.pb["value"] = i
                t0 = time.time()

            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        main_window.ConsoleFrame.push_text(f'Model Accuracy on test images: {round(100 * correct / total, 4)}')
        main_window.ConsoleFrame.epoch_text.set(f"Done!")
        main_window.NetworkFrame.train_button.config(state='normal')

    # Save the model checkpoint
    torch.save(model, save_model_as)
    # update the models in directory
    main_window.DrawFrame.scan_model_dir()
